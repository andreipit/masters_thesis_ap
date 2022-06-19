using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using InKin;

//https://habr.com/ru/post/332198/
//https://habr.com/ru/post/332164/

public class EntryPoint : MonoBehaviour
{
    public Vector3 ArmEndComputedPos;
    public Vector3 TrueEndPos;

    public List<RobotJoint> Joints;
    public float[] angles;

    public float[] anglesComputed;
    public Transform Target;


    public float DistanceThreshold = 0.01f;
    public float LearningRate = 100f;
    public int Epochs = 1;

    //void OnDrawGizmos()
    void Update()
    {


        TrueEndPos = Joints.Last().transform.position;
        //angles = Joints.Select(x => x.transform.localEulerAngles.x).ToArray();
        angles = Joints.Select(x => x.transform.localEulerAngles.x).ToArray();

        // find arm end position
        ArmEndComputedPos = Fwd.ForwardKinematics(angles, Joints);

        if (Target != null)
        {
            // angles for current arm end position
            anglesComputed = Inverse.InverseKinematics(Target.position, angles, Joints, DistanceThreshold, LearningRate, Epochs);
            for (int i = 0; i < Joints.Count; i++)
            {
                var rot = Joints[i].transform.localEulerAngles;
                Joints[i].transform.localEulerAngles = new Vector3(anglesComputed[i], rot.y, rot.z);
            }
        }
    }
}
