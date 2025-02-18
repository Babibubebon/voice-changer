import sys
import json
import os
import shutil
from typing import Union
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File, Form

from restapi.mods.FileUploader import upload_file, concat_file_chunks
from voice_changer.VoiceChangerManager import VoiceChangerManager

from const import MODEL_DIR, UPLOAD_DIR, ModelType
from voice_changer.utils.LoadModelParams import LoadModelParams


os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


class MMVC_Rest_Fileuploader:
    def __init__(self, voiceChangerManager: VoiceChangerManager):
        self.voiceChangerManager = voiceChangerManager
        self.router = APIRouter()
        self.router.add_api_route("/info", self.get_info, methods=["GET"])
        self.router.add_api_route("/performance", self.get_performance, methods=["GET"])
        self.router.add_api_route("/upload_file", self.post_upload_file, methods=["POST"])
        self.router.add_api_route("/concat_uploaded_file", self.post_concat_uploaded_file, methods=["POST"])
        self.router.add_api_route("/update_settings", self.post_update_settings, methods=["POST"])
        self.router.add_api_route("/load_model", self.post_load_model, methods=["POST"])
        self.router.add_api_route("/model_type", self.post_model_type, methods=["POST"])
        self.router.add_api_route("/model_type", self.get_model_type, methods=["GET"])
        self.router.add_api_route("/onnx", self.get_onnx, methods=["GET"])
        self.router.add_api_route("/merge_model", self.post_merge_models, methods=["POST"])
        self.router.add_api_route("/update_model_default", self.post_update_model_default, methods=["POST"])
        self.router.add_api_route("/update_model_info", self.post_update_model_info, methods=["POST"])
        self.router.add_api_route("/upload_model_assets", self.post_upload_model_assets, methods=["POST"])

    def post_upload_file(self, file: UploadFile = File(...), filename: str = Form(...)):
        try:
            res = upload_file(UPLOAD_DIR, file, filename)
            json_compatible_item_data = jsonable_encoder(res)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def post_concat_uploaded_file(self, filename: str = Form(...), filenameChunkNum: int = Form(...)):
        try:
            res = concat_file_chunks(UPLOAD_DIR, filename, filenameChunkNum, UPLOAD_DIR)
            json_compatible_item_data = jsonable_encoder(res)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def get_info(self):
        try:
            info = self.voiceChangerManager.get_info()
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def get_performance(self):
        try:
            info = self.voiceChangerManager.get_performance()
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def post_update_settings(self, key: str = Form(...), val: Union[int, str, float] = Form(...)):
        try:
            print("[Voice Changer] update configuration:", key, val)
            info = self.voiceChangerManager.update_settings(key, val)
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)
            print(sys.exc_info())

    def post_load_model(
        self,
        slot: int = Form(...),
        isHalf: bool = Form(...),
        params: str = Form(...),
    ):
        try:
            paramDict = json.loads(params)
            print("paramDict", paramDict)

            # Change Filepath
            newFilesDict = {}
            for key, val in paramDict["files"].items():
                if val != "-" and val != "":
                    uploadPath = os.path.join(UPLOAD_DIR, val)
                    storePath = os.path.join(UPLOAD_DIR, f"{slot}", val)
                    storeDir = os.path.dirname(storePath)
                    os.makedirs(storeDir, exist_ok=True)
                    shutil.move(uploadPath, storePath)
                    newFilesDict[key] = storePath
            paramDict["files"] = newFilesDict

            props: LoadModelParams = LoadModelParams(slot=slot, isHalf=isHalf, params=paramDict)

            info = self.voiceChangerManager.loadModel(props)
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def post_model_type(self, modelType: ModelType = Form(...)):
        try:
            info = self.voiceChangerManager.switchModelType(modelType)
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def get_model_type(self):
        try:
            info = self.voiceChangerManager.getModelType()
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def get_onnx(self):
        try:
            info = self.voiceChangerManager.export2onnx()
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def post_merge_models(self, request: str = Form(...)):
        try:
            print(request)
            info = self.voiceChangerManager.merge_models(request)
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def post_update_model_default(self):
        try:
            info = self.voiceChangerManager.update_model_default()
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def post_update_model_info(self, newData: str = Form(...)):
        try:
            info = self.voiceChangerManager.update_model_info(newData)
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)

    def post_upload_model_assets(self, params: str = Form(...)):
        try:
            info = self.voiceChangerManager.upload_model_assets(params)
            json_compatible_item_data = jsonable_encoder(info)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            print("[Voice Changer] ex:", e)
