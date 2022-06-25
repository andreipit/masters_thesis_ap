using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace InKin
{
    public class Inverse
    {


        public static float[] InverseKinematics(Vector3 target, float[] angles, List<RobotJoint> Joints, float DistanceThreshold, float LearningRate, int epochs)
        {
            //if (Dist.DistanceFromTarget(target, angles, Joints) < DistanceThreshold)
            //    return angles;
            for (int j = 0; j < epochs; j++)
            {
                for (int i = Joints.Count - 1; i >= 0; i--)
                {
                    // Градиентный спуск
                    // Обновление : Solution -= LearningRate * Gradient
                    float gradient = Grad.PartialGradient(target, angles, i, Joints);
                    angles[i] -= LearningRate * gradient;

                    // Ограничение
                    angles[i] = Mathf.Clamp(angles[i], Joints[i].MinAngle, Joints[i].MaxAngle);

                    //Преждевременное завершение
                    if (Dist.DistanceFromTarget(target, angles, Joints) < DistanceThreshold)
                        return angles;

                    //Debug.Log(1 + gradient);
                }
            }
            return angles;

        }

    }
}
