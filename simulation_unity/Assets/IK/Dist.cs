using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace InKin
{
    public class Dist
    {
        public static float DistanceFromTarget(Vector3 target, float[] angles, List<RobotJoint> Joints)
        {
            Vector3 point = Fwd.ForwardKinematics(angles, Joints);
            return Vector3.Distance(point, target);
        }
    }
}
