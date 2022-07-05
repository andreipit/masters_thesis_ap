from utils.imports.entry_point_import import *

def pixel_with_max_q_discrete():
    top_l = (0, 0, 'top_l') # arm-eye-view (camera looks TO arm face)
    top_r = (223, 0, 'top_r') # arm-eye-view (camera looks TO arm face)
    bottom_r = (223, 223, 'bottom_r') # arm-eye-view (camera looks TO arm face)
    bottom_l = (0, 223, 'bottom_l') # arm-eye-view (camera looks TO arm face)
    quarter = random.randrange(0, 4, 1) # randrange(0, 101, 2) # Even integer from 0 to 100 inclusive
    if quarter == 0: return top_l
    if quarter == 1: return top_r
    if quarter == 2: return bottom_r
    if quarter == 3: return bottom_l

def pixel_with_max_q():
    # random action
    px_x = random.randrange(0, 223, 1) # randrange(0, 101, 2) # Even integer from 0 to 100 inclusive
    px_y = random.randrange(0, 223, 1) # 0 1... 223
    return px_x, px_y      

def rotation_with_max_q():
    return float(random.randrange(1, 17, 1) * 22.5)
    

if __name__ == '__main__':
    env = Env01() #env = gym.make('environment:env-v1') # Env01()
    #env = gym.make('environment:env-v1') # Env01()
    s = env.reset() # s is ortho image 224x224
    env.render()
    done = False

    while not done:
        time.sleep(0.1)
        px_y, px_x, txt = pixel_with_max_q_discrete()
        print('type command: res - reset, ren - render, g - grasp pixel:', px_x, px_y, txt, ' q - quit')
        x = input()
        if x == 'g':
            pos3d = OrthTo3d().pixel_to_3d(px_x, px_y, s, env.r.m.heightmap_resolution, env.r.m.workspace_limits)
            degrees = rotation_with_max_q()
            a = np.asarray([1.0, pos3d[0], pos3d[1], pos3d[2], degrees])
            s, r, done, info = env.step(a)
        elif x == 'res':
            s = env.reset()
        elif x == 'ren':
            env.render()
        elif x == 'q':
            break 
    a: ArgsModel = ParserJson.convert_dict_to_vars(ParserJson.load_config(debug = False))

    #while not done:
    #    time.sleep(0.1)
    #    print('type command: 1 - test, q - quit, res - reset, ren - render, g - grasp, p - push')
    #    time.sleep(.1)
    #    x = input()
    #    if x == '1':
    #        print('1 was pressed')
    #    elif x == 'q':
    #        break 
    #    elif x == 'res':
    #        state = env.reset()
    #    elif x == 'ren':
    #        env.render()
    #    elif x == 'g':
    #        a_g = np.asarray([1.0, -0.5, 0, 0.25, 0]) # center of desk on height 0.2 grasp at (.5, .5, .5)
    #        s, r, done, info = env.step(a_g)
    #        env.total_r += r
    #    elif x == 'p':
    #        a_p = np.asarray([0.0, -0.5, -0.2, 0.25, 90]) # center of desk on height 0.2 grasp at (.5, .5, .5)
    #        s, r, done, info = env.step(a_p)




#elif x == 'photo':
#    bg_color_img: NDArray["480,640,3", np.uint8] = None
#    bg_depth_img: NDArray["480,640", float] = None
#    bg_color_img, bg_depth_img = r.sim.get_2_perspcamera_photos_480x640(r.m)

#    plt.imshow(bg_color_img)
#    plt.show(block=True)

#    plt.imshow(bg_depth_img)
#    plt.show(block=True)
#plt.plot([1, 2, 3], [1, 2, 3], '-.', c='red', label = 'bubble')
#plt.legend(loc="upper left")      
##plt.savefig('output.png')
#plt.show(block=True)

    
    
