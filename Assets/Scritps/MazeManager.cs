using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

public class MazeManager : MonoBehaviour
{
    public GameObject wallPrefab; 
    public int chunkSize = 10; 
    private Dictionary<Vector2, bool> generatedChunks = new Dictionary<Vector2, bool>(); 
    public GameObject player;
    public Tilemap floorTilemap; 
    public Tile floorTile; 
    public GameObject collectiblePrefab; 
    public float collectibleSpawnChance = 0.01f; 
    void Start()
    {
        Vector3 playerPosition = new Vector3(0, 0, 0); 
        player = Instantiate(player, playerPosition, Quaternion.identity);

        
        GenerateInitialChunks();
    }

    void Update()
    {
        Vector2 playerChunkCoord = CalculateChunkCoordinate(player.transform.position);
        GenerateSurroundingChunks(playerChunkCoord);
    }

    void GenerateInitialChunks()
    {
        Vector2 centerChunk = Vector2.zero;
        GenerateSurroundingChunks(centerChunk);
    }

    void GenerateSurroundingChunks(Vector2 centerChunk)
    {
        for (int x = -2; x <= 2; x++)
        {
            for (int y = -2; y <= 2; y++)
            {
                Vector2 chunkCoord = new Vector2(centerChunk.x + x, centerChunk.y + y);
                GenerateChunkAt(chunkCoord);
            }
        }
    }

    Vector2 CalculateChunkCoordinate(Vector3 position)
    {
        int x = Mathf.FloorToInt(position.x / chunkSize);
        int y = Mathf.FloorToInt(position.y / chunkSize);
        return new Vector2(x, y);
    }

    void GenerateChunkAt(Vector2 chunkCoordinate)
    {
        if (generatedChunks.ContainsKey(chunkCoordinate)) return;

        generatedChunks[chunkCoordinate] = true;

        Vector3Int basePosition = new Vector3Int((int)chunkCoordinate.x * chunkSize - chunkSize / 2, (int)chunkCoordinate.y * chunkSize - chunkSize / 2, 0);

        for (int x = 0; x < chunkSize; x++)
        {
            for (int y = 0; y < chunkSize; y++)
            {
                Vector3Int tilePosition = new Vector3Int(basePosition.x + x, basePosition.y + y, 0);
                floorTilemap.SetTile(tilePosition, floorTile); 
                bool isWall = Random.Range(0, 4) == 0;

                if (isWall)
                {
                    Instantiate(wallPrefab, tilePosition + new Vector3(0.5f, 0.5f, 0), Quaternion.identity, transform);
                }
                else if(Random.value < collectibleSpawnChance)
                {
                    Vector3 spawnPos = new Vector3(chunkCoordinate.x * chunkSize + x + 0.5f, chunkCoordinate.y * chunkSize + y + 0.5f, 0);
                    Instantiate(collectiblePrefab, spawnPos, Quaternion.identity, transform);
                }
            }
        }
    }

}