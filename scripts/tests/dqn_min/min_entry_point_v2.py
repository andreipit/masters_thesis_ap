from tests.dqn_min.importer import *

def loss_to_f(loss:torch.Tensor) -> float:
    return loss.data.cpu().item()

def start():
    env, NN, NN_frozen, opt, ex_ex, log = create_objects_legacy()
    
    s = env.reset()
    for i in range(log.EPOCHS): # epochs count, epoch = month, salary = mean daily income
        month_money = []
        month_losses = []
        for j in range(log.SESSIONS): # sessions count, session = taxi work day
            total_reward = 0
            day_losses = []
            s = env.reset()
            n_actions = env.action_space.n
            for t in range(log.STEPS):
                a = get_action(s, NN, ex_ex)
                s2, r, done, info = env.step(a)
                #env.render()
                opt.zero_grad()
                loss = td_loss([s], [a], [r], [s2], [done], NN, NN_frozen) # => tensor(1.0086, grad_fn=<MeanBackward0>)
                loss.backward()
                opt.step()
                if t % 100 == 0: NN_frozen.load_state_dict(NN.state_dict())
                total_reward += r
                day_losses.append(loss.data.cpu().item()) # 1.0085, when order_loss==tensor(1.0086, grad_fn=<MeanBackward0>)
                s = s2
                if done:
                    break
            day_total_money = total_reward
            day_mean_loss = np.mean(day_losses)
            month_money.append(day_total_money)
            month_losses.append(day_mean_loss)
        if ex_ex > 0.01: ex_ex *= (1 - 1e-2) # Lower epsilon => less often we choose random # 
        month_salary = np.mean(month_money)
        print('epoch:', i, 'mean r:', month_salary, 'epsilon:', ex_ex)
        if month_salary > 300:
            print("You Win!")
            break



if __name__ == '__main__':
    start()