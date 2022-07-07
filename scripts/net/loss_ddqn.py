from net.importer import *

def td_loss_double_dqn(
    s:list, a:list, r:list, s2:list, done:list, 
    agent, target_net, gamma=0.99, device=device):
    """ Suppose there are 10 steps in session => batch size == 10 ==> s=(s0,...,s9), a=(a0,...,a9) """
    s,a,r,s2,done = _convert_batches_to_tensors_batches(s,a,r,s2,done) # each var is BATCH!!! [batch_size, *state_shape]
    
    # 1) our prediction
    s_qvalues = agent(s) # get all salaries in current city                                        #=>(do it for 10 cities in batch)
    s_a_qvalue = s_qvalues[range(s.shape[0]), a] # PRED = choose salary of our driver from them               #=>(do it for 10 drivers we've used)
    
    # 2) true value
    s2_qvalues =  agent(s2) # get all salaries in next city                                #=>(do it for 10 next_cities in batch)
    s2_qvalues_frozen =  target_net(s2) # get all salaries in next city                                #=>(do it for 10 next_cities in batch)
    
    
    s2_value = s2_qvalues_frozen.gather(1, torch.max(s2_qvalues, 1)[1].unsqueeze(1)).squeeze(1)
    
    #s2_value = torch.max(s2_qvalues, dim=1)[0] # city2_value=max_salary (bellman->expected final)   #=>(do it for 10 next_cities in batch)
    
    
    truth_target = r + gamma * s2_value # HALF-TRUE = [game signal] + g*[prediction starting from next city] #=> 10rewards + 10s2_values
    # if done: truth = r + gamma*0 = r, cause s2 doesn't exist!
    # torch.where(torch.tensor([0,1,1], dtype=torch.uint8), torch.tensor([7, 7, 7], dtype=torch.uint8), torch.tensor([8, 8, 8], dtype=torch.uint8))
    #===> tensor([8, 7, 7], dtype=torch.uint8)
    truth_target = torch.where(done, r, truth_target) # at the last state we shall use simplified formula: Q(s,a) = r(s,a) since s' doesn't exist
    
    # 3) loss = pred - true = float wraped in tensor
    loss = torch.mean( (s_a_qvalue - truth_target.detach())** 2 ) # detach, cause frozen                           #=> (10preds - 10true)**2 / 10
    return loss


def _convert_batches_to_tensors_batches(s,a,r,s2,done):
    s = torch.tensor(s, device=device, dtype=torch.float32)    # shape: [batch_size, state_size]
    a = torch.tensor(a, device=device, dtype=torch.long)    # shape: [batch_size]
    r = torch.tensor(r, device=device, dtype=torch.float32)  # shape: [batch_size]
    s2 = torch.tensor(s2, device=device, dtype=torch.float32)
    done = torch.tensor(done, device=device, dtype=torch.uint8)  # shape: [batch_size]
    return s,a,r,s2,done

#def compute_td_loss(batch_size):
#    state, action, reward, next_state, done = replay_buffer.sample(batch_size)

#    state      = Variable(torch.FloatTensor(np.float32(state)))
#    next_state = Variable(torch.FloatTensor(np.float32(next_state)))
#    action     = Variable(torch.LongTensor(action))
#    reward     = Variable(torch.FloatTensor(reward))
#    done       = Variable(torch.FloatTensor(done))

#    q_values      = current_model(state)
#    next_q_values = current_model(next_state)
#    next_q_state_values = target_model(next_state) 

#    q_value       = q_values.gather(1, action.unsqueeze(1)).squeeze(1) 
#    next_q_value = next_q_state_values.gather(1, torch.max(next_q_values, 1)[1].unsqueeze(1)).squeeze(1)
#    expected_q_value = reward + gamma * next_q_value * (1 - done)
    
#    loss = (q_value - Variable(expected_q_value.data)).pow(2).mean()
        
#    optimizer.zero_grad()
#    loss.backward()
#    optimizer.step()
    
#    return loss
