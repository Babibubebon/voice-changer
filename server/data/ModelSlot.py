from typing import TypeAlias, Union
from const import MAX_SLOT_NUM, EnumInferenceTypes, EnumEmbedderTypes, VoiceChangerType

from dataclasses import dataclass, asdict

import os
import json


@dataclass
class ModelSlot:
    voiceChangerType: VoiceChangerType | None = None


@dataclass
class RVCModelSlot(ModelSlot):
    voiceChangerType: VoiceChangerType = "RVC"
    modelFile: str = ""
    indexFile: str = ""
    defaultTune: int = 0
    defaultIndexRatio: int = 1
    defaultProtect: float = 0.5
    isONNX: bool = False
    modelType: str = EnumInferenceTypes.pyTorchRVC.value
    samplingRate: int = -1
    f0: bool = True
    embChannels: int = 256
    embOutputLayer: int = 9
    useFinalProj: bool = True
    deprecated: bool = False
    embedder: str = EnumEmbedderTypes.hubert.value

    name: str = ""
    description: str = ""
    credit: str = ""
    termsOfUseUrl: str = ""
    sampleId: str = ""
    iconFile: str = ""


ModelSlots: TypeAlias = Union[ModelSlot, RVCModelSlot]


def loadSlotInfo(model_dir: str, slotIndex: int) -> ModelSlots:
    slotDir = os.path.join(model_dir, str(slotIndex))
    jsonFile = os.path.join(slotDir, "params.json")
    if not os.path.exists(jsonFile):
        return ModelSlot()
    jsonDict = json.load(open(os.path.join(slotDir, "params.json")))
    slotInfo = ModelSlot(**{k: v for k, v in jsonDict.items() if k in ModelSlot.__annotations__})
    if slotInfo.voiceChangerType == "RVC":
        return RVCModelSlot(**jsonDict)
    else:
        return ModelSlot()


def loadAllSlotInfo(model_dir: str):
    slotInfos: list[ModelSlots] = []
    for slotIndex in range(MAX_SLOT_NUM):
        slotInfo = loadSlotInfo(model_dir, slotIndex)
        slotInfos.append(slotInfo)
    return slotInfos


def saveSlotInfo(model_dir: str, slotIndex: int, slotInfo: ModelSlots):
    slotDir = os.path.join(model_dir, str(slotIndex))
    json.dump(asdict(slotInfo), open(os.path.join(slotDir, "params.json"), "w"))
