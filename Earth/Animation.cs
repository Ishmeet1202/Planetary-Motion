using TMPro;
using UnityEngine;



public class Rotate : MonoBehaviour
{
    float alpha = 0;
    private float xaxis, yaxis, a = 18, b = 20;
    public TrailRenderer trail;
    public GameObject Sun;
    private Vector3 offset = new Vector3(0, 10, 0);
    
    public Camera MainCamera;
    public enum Planet
    {
        Sun,
        Earth
    }

    public Planet GetPlanet;

    void Update()
    {

        if (GetPlanet == Planet.Earth)
        {

            transform.Rotate(0, 0.5f, 0, Space.Self);
            alpha += 0.5f;
            xaxis = Sun.transform.position.x;
            yaxis = Sun.transform.position.z;
            float X = xaxis + (a * Mathf.Cos(alpha * .005f));
            float Z = yaxis + (b * Mathf.Sin(alpha * .005f));
            gameObject.transform.position = new Vector3(X, 0, Z);
            trail.transform.position = gameObject.transform.position;
           
       

        }
        if (GetPlanet == Planet.Sun)
        {
          

            transform.Rotate(0, 0.5f, 0, Space.Self);


        




        }

           

    }

   
        
    
}
