using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class InfoController : MonoBehaviour
{
    public TextMeshProUGUI timeText;
    public TextMeshProUGUI scoreText;
    void Start()
    {
        float time = PlayerPrefs.GetFloat("time", 0);
        timeText.text = "Time played: " + Mathf.FloorToInt(time / 60).ToString("00") + ":" + Mathf.FloorToInt(time % 60).ToString("00");
        scoreText.text = "Slain Enemies: " + PlayerPrefs.GetInt("slainEnemies", 0).ToString();
        
    }

}
