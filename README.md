# MCOC2020-P1
# Entrega 1 - Integración de ecuaciones diferenciales
- ![image](https://user-images.githubusercontent.com/43451947/91111616-fa560380-e64e-11ea-9730-1997954eb9eb.png)
# Entrega2 - Primeras predicciones con la EDM básica del satélite
- ![image](https://user-images.githubusercontent.com/43451947/91516562-d1857680-e8b9-11ea-8924-3ccf8a7b0753.png)
- ![image](https://user-images.githubusercontent.com/43451947/91516595-e6620a00-e8b9-11ea-8eeb-7cb335a26baf.png)
# Entrega5 - Mejoras al modelo y estudio de convergencia
- Pregunta 1:
  - Grafico resultado: ![image](https://user-images.githubusercontent.com/43451947/92336431-c62f0980-f076-11ea-9fee-5d2e557030ea.png)
- Pregunta 2:
  - Grafico resultado: ![image](https://user-images.githubusercontent.com/43451947/92336455-45244200-f077-11ea-8122-715daab5477b.png)
  - Como se puede ver en el grafico, para eulerint con Nsubdivisiones = 1, la deriva con respecto a la prediccion de odeint sin mejoras es de: 19226.4 - 2094.1 Km, es decir, la deriva es de:  17.132,3 Km al final del tiempo.
  - El tiempo que toma odeint en producir los resultados es de: 0.1689461999339983 segundos
  - El tiempo que toma eulerint en producir los resultados es de: 0.475070400047116 segundos
- Pregunta 3:
  - Grafico resultado:
  
  ![image](https://user-images.githubusercontent.com/43451947/92338312-f03bf800-f085-11ea-9cb4-21aeaca907a1.png)
  - A partir del grafico se puede apreciar que para eulerint con Nsubdivisiones = 10000 se acerca bastante al resultado de odeint, pero aun le falta para ser exacto.
  En mi caso con esta cantidad de subdivisiones el error fue de 5.3957092911654305 %,para verificar esto, la deriva de odeint fue de 2094113.4262998656 metros, mientras que la de eulerint fue de 1981121.153589461 metros. Con un tiempo de ejecucion del codigo de 1.3012106068333378 horas.
  Como el tiempo de ejecucion fue bastante largo, no quise aumentar el numero de subdivisiones debido a que iba a estar horas y horas tratando de averiguar la cantidad de subdivisiones para que fuese menor a un 1%, pero puedo decir que con alrededor de Nsubdivisiones = 100000 deberia estar en menos el 1% de error, siendo que el tiempo de ejecucion es lineal con respecto a la cantidad de subdivisiones, habria tomado cerca de 13 horas de ejecucion para esta cantidad de subdivisiones en mi computador, ya que este tiempo para cada computador es diferente.
- Pregunta 4:
  - Graficos resultados:
  
  ![image](https://user-images.githubusercontent.com/43451947/92336595-b57f9300-f078-11ea-86b0-6d7612492466.png)
  
  ![image](https://user-images.githubusercontent.com/43451947/92336598-bd3f3780-f078-11ea-885e-607b9770ed76.png)
  
  ![image](https://user-images.githubusercontent.com/43451947/92336603-c3cdaf00-f078-11ea-969d-31dce258849e.png)
  
  ![image](https://user-images.githubusercontent.com/43451947/92336613-d1833480-f078-11ea-89f7-386112229782.png)

  - Como se puede apreciar en los graficos, ocurrio algo bastante interesante en mi caso, el cual fue que aplicando la mejora de J2, la deriva de la posicion final fue de 4.3 Km, mientras que cuando se aplico la mejora de J2 y J3, la deriva aumento un poco siendo esta de 6.6 Km lo que fue inusual porque se supone que deberia disminuir el error, pero esto se puede deber a que no todos los archivos EOF son iguales, lo puedo verificar por el hecho que el profesor cuando corrio los codigos en su computador pasaba lo mismo.
  - Para el caso de la mejora J2: El tiempo que toma al codigo producir los resultados es de: 1.1903783000307158 segundos
  - Para el caso de la mejora J2 y J3: El tiempo que toma al codigo producir los resultados es de: 1.4467591000720859 segundos
  - Cabe destacar que estos tiempos oscilan, y van aproximadamente del rango de 1.15 a 1.5 segundos, pero no mas ni menos que eso, siendo estos bastante parecidos.
