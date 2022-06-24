using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;
using System.Threading;

public class TestTCP : MonoBehaviour
{
    // visualization
    public enum States { Checking, Connected, NotConnected }

    [Header("Check connection:")]
    public bool ActivateCheck;
    public States state;
    public bool Connected;
    public string LastReceived; // changes only if smth received
    public float LastReceivedTime; // changes only if smth received

    [Header("Send to server:")]
    public bool SendButton;
    public string SendMes = "send smth";
    public bool Delivered;
    public float DeliveredTime;
    public float FailDeliveredTime;
    public string LastServerAnswer;

    // async check returns
    bool m_CheckIsRunning = false; // to be sure that we run only 1 check
    int m_IsConnected = -1; // -1 undifined, 0 not, 1 connected

    // timers
    float m_LastSuccessTime = -1;
    float m_Timer = -1;


    private void Start()
    {
        m_Timer = Time.time;
        m_LastSuccessTime = Time.time;
    }

    void Update()
    {
        if (ActivateCheck)
        {
            ConnectAndReceive();
        }

        if (SendButton)
        {
            SendButton = false;
            SendMessage(SendMes);
        }
    }

    async void SendMessage(string _Mes, bool _Debug = false)
    {
        byte[] mes = System.Text.Encoding.ASCII.GetBytes(_Mes); // string someString = Encoding.ASCII.GetString(bytes);
        //string result = MyTCPClientLibrary.SendAndReceive(mes);
        string result = "";
        try { result = await Task.Run(() => MyTCPClientLibrary.SendAndReceive(mes)); } catch { }

        LastServerAnswer = result;

        if (result == "I_have_received_" + _Mes)
        {
            Delivered = true;
            DeliveredTime = Time.time;
        }
        else
        {
            Delivered = false;
            FailDeliveredTime = Time.time;
        }
    }

    void ConnectAndReceive()
    {
        // 1) Check connection
        if (!m_CheckIsRunning)
        {
            m_CheckIsRunning = true;
            CheckConnection();
        }
        if (m_IsConnected == -1) state = States.Checking;
        else if (m_IsConnected == 0) state = States.NotConnected;
        else if (m_IsConnected == 1)
        {
            state = States.Connected;
            m_LastSuccessTime = Time.time; // reset our timer, we have 2 extra secs
        }

        // 2) Show warning if not connected for a long time
        Connected = (Time.time - m_LastSuccessTime < 1); // if no success 2 secs -> means not connected
    }

    /// <summary> connection sanity check each second: send - receive </summary>
    async void CheckConnection(float _Pause = 0.1f, bool _Debug = false)
    {
        // 1) wait 1 sec
        if (Time.time - m_Timer < _Pause)
        {
            m_CheckIsRunning = false; // allow next check
            return;
        }
        m_Timer = Time.time;
        m_IsConnected = -1;
        if (_Debug) Debug.Log("Check start");

        // 2) prepare message and result
        byte[] mes = System.Text.Encoding.ASCII.GetBytes("{key1:hello, key2:world}"); // string someString = Encoding.ASCII.GetString(bytes);

        // 3) send and receive
        string result = "";
        try { result = await Task.Run(() => MyTCPClientLibrary.SendAndReceive(mes)); } catch { }
        if (_Debug) Debug.Log("Check end result = " + result + ", is empty = "+ (result==""));

        // 4) return (by global vars, cause async)
        m_CheckIsRunning = false; // allow next check
        m_IsConnected = (result == "") ? 0 : 1;
        LastReceived = (result == "") ? LastReceived : result; // changes only if smth received
        LastReceivedTime = (result == "") ? LastReceivedTime : Time.time; // changes only if smth received
    }
}


// 4) handle server answer
//if (result == "html.reset")
//{
//    Debug.Log("reset happend");

//    var node = GameObject.Find("node_00");
//    var nodes = node.GetComponentsInChildren<InKin.RobotJoint>();
//    Debug.Log("node=" + node);
//    Debug.Log("nodes count=" + nodes.Length);
//    foreach (InKin.RobotJoint j in nodes)
//    {
//        Debug.Log("joint:" + j.name);
//        j.transform.localEulerAngles = Vector3.zero;
//    }
//}
