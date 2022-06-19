using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace InKin
{
    public class RobotJoint : MonoBehaviour
    {
        public Vector3 Axis;
        public Vector3 StartOffset;

        public float MinAngle;
        public float MaxAngle;

        //void OnDrawGizmos()
        void Update()
        {
            StartOffset = transform.localPosition;
            Axis = new Vector3(1, 0, 0);
            MinAngle = 0f;
            MaxAngle = 360f;
        }
    }
}