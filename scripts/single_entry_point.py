from utils.imports.entry_point_import import *

if __name__ == '__main__':
    print('hi')
    a: ArgsModel = ParserJson.convert_dict_to_vars(ParserJson.load_config(debug = False))
    env = Env01() #env = gym.make('environment:env-v1') # Env01()
    state = env.reset()
    env.render()
    done = False

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
            a_g = np.asarray([1.0, -0.5, 0, 0.25, 0]) # center of desk on height 0.2 grasp at (.5, .5, .5)
            s, r, done, info = env.step(a_g)
            env.total_r += r
        elif x == 'p':
            a_p = np.asarray([0.0, -0.5, -0.2, 0.25, 90]) # center of desk on height 0.2 grasp at (.5, .5, .5)
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

    
    
