using System.Collections;
using System.Collections.Generic;
using UnityEngine;


//https://habr.com/ru/post/332198/
//https://habr.com/ru/post/332164/

namespace InKin
{

    public class Fwd : MonoBehaviour
    {

        /// <summary>
        /// Find arm end position
        /// </summary>
        /// <param name="angles"> Actuators x angles </param>
        /// <param name="Joints"> Actuators wrap </param>
        /// <returns></returns>
        public static Vector3 ForwardKinematics(float[] angles, List<RobotJoint> Joints)
        {
            Vector3 res = Joints[0].transform.position;
            Quaternion rotation = Quaternion.identity;
            for (int i = 1; i < Joints.Count; i++)
            {
                // Выполняет поворот вокруг новой оси
                rotation *= Quaternion.AngleAxis(angles[i - 1], Joints[i - 1].Axis);
                Vector3 nextPoint = res + rotation * Joints[i].StartOffset;

                res = nextPoint;
            }
            return res;
        }
    }
}
