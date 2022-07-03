from utils.imports.entry_point_import import *

if __name__ == '__main__':
    print('hi')
    a: ArgsModel = ParserJson.convert_dict_to_vars(ParserJson.load_config(debug = False))
    env = Env01() #env = gym.make('environment:env-v1') # Env01()
    state = env.reset()
    env.render()
    done = False
    #a_g = [1.0, -0.6, -0.3, 0.1, 120] # center of desk on height 0.2 grasp at (.5, .5, .5)
    #a_g = np.asarray([1.0, -0.6, -0.3, 0.1, 120]) # center of desk on height 0.2 grasp at (.5, .5, .5)
    a_g = np.asarray([1.0, -0.5, 0, 0.25, 0]) # center of desk on height 0.2 grasp at (.5, .5, .5)
    #a_g2 = [1.0, -0.2, 0.3, 0.1, 120] # center of desk on height 0.2 grasp at (.5, .5, .5)
    #a_g2 = np.asarray([1.0, -0.2, 0.3, 0.1, 120]) # center of desk on height 0.2 grasp at (.5, .5, .5)
    a_p = np.asarray([0.0, -0.6, 0, 0.1, 120]) # center of desk on height 0.2 grasp at (.5, .5, .5)
    #once = True
    #s, r, done, info = env.step(a_g)
    while not done:
        time.sleep(0.1)
        print('type command: 1 - test, q - quit, res - reset, ren - render, g - grasp, p - push')
        time.sleep(.1)
        x = input()
        if x == '1':
            print('1 was pressed')
        elif x == 'q':
            break 
        elif x == 'res':
            state = env.reset()
        elif x == 'ren':
            env.render()
        elif x == 'g':
            #y = input()
            #a_g[4] = float(y)
            #a_g2[4] = float(y)
            s, r, done, info = env.step(a_g)
            env.total_r += r
            #if once:
                #s, r, done, info = env.step(a_g)
            #    once = False
            #else:
            #s, r, done, info = env.step(a_g2)
                #once = True
        elif x == 'p':
            s, r, done, info = env.step(a_p)


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

    
    
