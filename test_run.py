from run import *

def test_welcome():

     # available files to practice
    file_names = ["Die90haeufigstenVerbenA1",
              "VerbenNiveauA2-B1",
              "SportundFreizeit",
              "HaeufigkeitundReihenfolge",
              "KoerperlicheTaetigkeiten",
              "AeusseresErscheinungsbild",
              "CharakterAndTemperament",
              "Zeitangaben"
              ]
    
    mtk = tk(file_names)
    run(mtk)