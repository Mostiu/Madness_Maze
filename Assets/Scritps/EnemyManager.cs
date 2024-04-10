using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyManager : MonoBehaviour
{
    public GameObject enemyPrefab; 
    public float spawnRate = 30.0f; 
    private float nextSpawnTime = 0.0f;
    private GameObject player;


    private void Start()
    {
        spawnRate = PlayerPrefs.GetFloat("spawnRate", 10.0f);
        player = GameObject.FindGameObjectWithTag("Player");
    }

    void Update()
    {
        if (Time.time >= nextSpawnTime)
        {
            SpawnEnemy();
            nextSpawnTime = Time.time + spawnRate;
        }
    }

    void SpawnEnemy()
    {
        Vector3 spawnPosition = Vector3.zero;
        bool validSpawnPosition = false;

        while (!validSpawnPosition)
        {
            spawnPosition = player.transform.position + new Vector3(Random.Range(-10, 10), Random.Range(-10, 10), 0);

            if (!Physics2D.OverlapCircle(spawnPosition, 0.5f)) 
            {
                validSpawnPosition = true;
            }
        }

        Instantiate(enemyPrefab, spawnPosition, Quaternion.identity);
    }
}

