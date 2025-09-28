export const enum TrainType {
  AVE = "AVE",
  EUROCITY = "EuroCity",
  EUROSTAR = "Eurostar",
  FRECCIAROSSA = "Frecciarossa",
  IC = "IC",
  ICE = "ICE",
  INTERCITY = "InterCity",
  INTERCITES = "Intercités",
  ITALO = "Italo",
  NIGHTJET = "Nightjet",
  RE = "RE",
  RJX = "RJX",
  RAILJET = "Railjet",
  REGIOEXPRESS = "RegioExpress",
  TER = "TER",
  TGV = "TGV",
  THALYS = "Thalys"
}

export const trainTypeFromRaw: Record<string, TrainType> = {
  "AVE": TrainType.AVE,
  "EuroCity": TrainType.EUROCITY,
  "Eurostar": TrainType.EUROSTAR,
  "Frecciarossa": TrainType.FRECCIAROSSA,
  "IC": TrainType.IC,
  "ICE": TrainType.ICE,
  "InterCity": TrainType.INTERCITY,
  "Intercités": TrainType.INTERCITES,
  "Italo": TrainType.ITALO,
  "Nightjet": TrainType.NIGHTJET,
  "RE": TrainType.RE,
  "RJX": TrainType.RJX,
  "Railjet": TrainType.RAILJET,
  "RegioExpress": TrainType.REGIOEXPRESS,
  "TER": TrainType.TER,
  "TGV": TrainType.TGV,
  "Thalys": TrainType.THALYS
};

