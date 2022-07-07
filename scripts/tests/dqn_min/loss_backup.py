from tests.dqn_min.importer import *


def td_loss_SUPER_BEST_WITH_FROZEN(states, actions, rewards, next_states, is_done, network, NN_frozen, gamma=0.99, check_shapes=False):
    """ Compute td loss using torch operations only. Use the formula above. """
    states = torch.tensor(
        states, device=device, dtype=torch.float32)    # shape: [batch_size, state_size]
    actions = torch.tensor(actions, device=device, dtype=torch.long)    # shape: [batch_size]
    rewards = torch.tensor(rewards, device=device, dtype=torch.float32)  # shape: [batch_size]
    # shape: [batch_size, state_size]
    next_states = torch.tensor(next_states, device=device, dtype=torch.float32)
    is_done = torch.tensor(is_done, device=device, dtype=torch.uint8)  # shape: [batch_size]

    # get q-values for all actions in current states
    predicted_qvalues = network(states)

    # select q-values for chosen actions
    predicted_qvalues_for_actions = predicted_qvalues[
      range(states.shape[0]), actions
    ]

    # compute q-values for all actions in next states
    predicted_next_qvalues = NN_frozen(next_states)

    # compute V*(next_states) using predicted next q-values
    next_state_values = torch.max(predicted_next_qvalues, dim=1)[0]
    assert next_state_values.dtype == torch.float32

    # compute "target q-values" for loss - it's what's inside square parentheses in the above formula.
    target_qvalues_for_actions = rewards + gamma * next_state_values

    # at the last state we shall use simplified formula: Q(s,a) = r(s,a) since s' doesn't exist
    target_qvalues_for_actions = torch.where(
        is_done, rewards, target_qvalues_for_actions)

    # mean squared error loss to minimize
    loss = torch.mean((predicted_qvalues_for_actions -
                       target_qvalues_for_actions.detach()) ** 2)

    if check_shapes:
        assert predicted_next_qvalues.data.dim(
        ) == 2, "make sure you predicted q-values for all actions in next state"
        assert next_state_values.data.dim(
        ) == 1, "make sure you computed V(s') as maximum over just the actions axis and not all axes"
        assert target_qvalues_for_actions.data.dim(
        ) == 1, "there's something wrong with target q-values, they must be a vector"

    return loss

def td_loss_GOOD_BUT_WITHOUT_FROZEN(states, actions, rewards, next_states, is_done, network, gamma=0.99, check_shapes=False):
    """ Compute td loss using torch operations only. Use the formula above. """
    states = torch.tensor(
        states, device=device, dtype=torch.float32)    # shape: [batch_size, state_size]
    actions = torch.tensor(actions, device=device, dtype=torch.long)    # shape: [batch_size]
    rewards = torch.tensor(rewards, device=device, dtype=torch.float32)  # shape: [batch_size]
    # shape: [batch_size, state_size]
    next_states = torch.tensor(next_states, device=device, dtype=torch.float32)
    is_done = torch.tensor(is_done, device=device, dtype=torch.uint8)  # shape: [batch_size]

    # get q-values for all actions in current states
    predicted_qvalues = network(states)

    # select q-values for chosen actions
    predicted_qvalues_for_actions = predicted_qvalues[
      range(states.shape[0]), actions
    ]

    # compute q-values for all actions in next states
    predicted_next_qvalues = network(next_states)

    # compute V*(next_states) using predicted next q-values
    next_state_values = torch.max(predicted_next_qvalues, dim=1)[0]
    assert next_state_values.dtype == torch.float32

    # compute "target q-values" for loss - it's what's inside square parentheses in the above formula.
    target_qvalues_for_actions = rewards + gamma * next_state_values

    # at the last state we shall use simplified formula: Q(s,a) = r(s,a) since s' doesn't exist
    target_qvalues_for_actions = torch.where(
        is_done, rewards, target_qvalues_for_actions)

    # mean squared error loss to minimize
    loss = torch.mean((predicted_qvalues_for_actions -
                       target_qvalues_for_actions.detach()) ** 2)

    if check_shapes:
        assert predicted_next_qvalues.data.dim(
        ) == 2, "make sure you predicted q-values for all actions in next state"
        assert next_state_values.data.dim(
        ) == 1, "make sure you computed V(s') as maximum over just the actions axis and not all axes"
        assert target_qvalues_for_actions.data.dim(
        ) == 1, "there's something wrong with target q-values, they must be a vector"

    return loss


def td_loss2_NOT_WORKING(
    s:list, a:list, r:list, s2:list, done:list, 
    agent, target_net, gamma=0.99, device=device):
    """ Suppose there are 10 steps in session => batch size == 10 ==> s=(s0,...,s9), a=(a0,...,a9) """
    s,a,r,s2,done = _convert_batches_to_tensors_batches(s,a,r,s2,done) # each var is BATCH!!! [batch_size, *state_shape]
    # 1) our prediction
    pred_s_all = agent(s) # get all salaries in current city                                        #=>(do it for 10 cities in batch)
    pred = pred_s_all[range(len(a)), a] # PRED = choose salary of our driver from them               #=>(do it for 10 drivers we've used)
    # 2) true value
    pred_s2_all =  target_net(s2) # get all salaries in next city                                #=>(do it for 10 next_cities in batch)
    s2_value = torch.max(pred_s2_all, dim=1)[0] # city2_value=max_salary (bellman->expected final)   #=>(do it for 10 next_cities in batch)
    true = r + gamma * s2_value # HALF-TRUE = [game signal] + g*[prediction starting from next city] #=> 10rewards + 10s2_values
    # 3) loss = pred - true = float wraped in tensor
    loss = torch.mean( (pred - true.detach())** 2 ) # detach, cause frozen                           #=> (10preds - 10true)**2 / 10
    return loss

def _convert_batches_to_tensors_batches_legacy_BAD(s,a,r,s2,done):
    #print('device',device)
    s = torch.tensor(s, device=device, dtype=torch.float32)    # shape: [batch_size, *state_shape]
    a = torch.tensor(a, device=device, dtype=torch.int64)    # shape: [batch_size]
    r = torch.tensor(r, device=device, dtype=torch.float32)  # shape: [batch_size]
    s2 = torch.tensor(s2, device=device, dtype=torch.float32) # shape: [batch_size, *state_shape]
    done = np.asarray(done)
    done = torch.tensor(done.astype('float32'), device=device, dtype=torch.float32)  # shape: [batch_size]
    return s,a,r,s2,done

