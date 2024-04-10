using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

public class ConfigManager : MonoBehaviour
{
    public Color pressedColor = Color.green;
    public Color normalColor = Color.red;
    public Button fewerEnemiesButton;
    public Button moreEnemiesButton;


    private float fewerSpawnRate = 20.0f;
    private float moreSpawnRate = 10.0f;

    public  void SetFewerEnemies()
    {
        PlayerPrefs.SetFloat("spawnRate", fewerSpawnRate);
        fewerEnemiesButton.GetComponent<Image>().color = pressedColor;
        moreEnemiesButton.GetComponent<Image>().color = normalColor;
    }

    public void SetMoreEnemies()
    {
        PlayerPrefs.SetFloat("spawnRate",moreSpawnRate);
        fewerEnemiesButton.GetComponent<Image>().color = normalColor;
        moreEnemiesButton.GetComponent<Image>().color = pressedColor;
    }
}
