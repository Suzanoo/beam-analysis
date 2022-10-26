## **Continuous Beam Analysis(Stiffness Matrix Method)**
This app adopt from [Prof. Fredy Gabriel Ramírez Villanueva](https://github.com/SirPrime/MatrixAnalysis-Beams.git)  repository

And from Youtube channel  [วิเคราะห์โครงสร้างกับ อ.กิจ](www.youtube.com/watch?v=hCmXwMQWafk&list=LL&index=6&t=3642s)

### How to use this app?

Open Terminal(Mac) or Command promp(Windows) os Anaconda promp(Cross platform) and follow these.

1.Install Python, Git, Anaconda
- [Python](https://www.python.org/downloads/)
- [Git](https://github.com/git-guides/install-git)
- [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)

2.Go to a folder you want to save this one.

3.Create conda env and then activate it
``` 
conda env list
conda create --name <your env name> python=3.10
conda activate <your env name>
```
4.Clone this repository
```
git clone https://github.com/Suzanoo/beam-analysis.git
```
5.Install package
```
pip install -r requirements.txt
```
6.Run app
```
shiny run --reload app.py
```

App will render SFD and BMD and you can save it.

You can see example from beam_analysis_example.pdf.