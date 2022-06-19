using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace InKin
{
    class Grad : MonoBehaviour
    {
        public static float SamplingDistance = 0.1f;

        public static float PartialGradient(Vector3 target, float[] angles, int i, List<RobotJoint> Joints)
        {
            // ��������� ����,
            // ������� ����� ������������ �����
            float angle = angles[i];

            // ��������: [F(x+SamplingDistance) - F(x)] / h
            float f_x = Dist.DistanceFromTarget(target, angles, Joints);

            angles[i] += SamplingDistance;
            float f_x_plus_d = Dist.DistanceFromTarget(target, angles, Joints);

            float gradient = (f_x_plus_d - f_x) / SamplingDistance;

            // ��������������
            angles[i] = angle;

            return gradient;
        }


    }
}
