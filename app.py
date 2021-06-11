from flask import Flask, render_template, jsonify, request, abort, Response
import requests
from server_utils import server_logger
import os
from cut_video import cut_video
from detect import inference
import base64
from PIL import Image
import io
import json
import zipfile
import os
from flask import send_file
import threading
import numpy as np

logger = server_logger.get_logger(__name__)
app = Flask(__name__)
logger.info("Initiating...")




import os, shutil
def delete_folder_content(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def getImageBytes(filePath):
    img = Image.open(filePath, mode='r')
    imgByteArr = io.BytesIO()
    print("imgByteArr:",imgByteArr)
    imgByteArr = imgByteArr.getvalue()
    print("imgByteArr:",imgByteArr)
    imgByteArr = base64.encodebytes(imgByteArr).decode('ascii')
    print("imgByteArr:",imgByteArr)
    return imgByteArr

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/get_video', methods=['POST'])
def receive_video():
    try:
        
        video = request.files.get('video', None)
        video_name = video.filename.split('.')[0]
        print("filename:",video_name)
        #logger.info(video)
        video.save(video.filename)

        def process_video(video_filename):
            video_name = video.filename.split('.')[0]
            if (os.path.exists(video_name)):
                delete_folder_content(video_name)
            else:
                os.mkdir(video_name)

            
            #delete_folder_content('images')
            cut_video(video.filename)
            
            
            infer_result = video_name+"_result"
            if (os.path.exists(infer_result)):
                delete_folder_content(infer_result)
            else:
                os.mkdir(infer_result)
            

            #delete_folder_content('infer_result/')
            infer = inference(source=video_name+"/",project=infer_result+"/")
            print("app:",infer)
            
            
            for item in infer:
                #print("item:",get_response_image(item[5]))
                #item[5] = get_response_image(item[5])
                item[5] = item[5].split('/')[-1]
                #item[5] = getImageBytes
            print("infer type:",type(infer))
            infer_numpy = np.array(infer)
            #with open(infer_result+'/result.txt','w') as outfile:
            #    json.dump(infer,outfile)
            np.savetxt(infer_result+'/result.txt',infer_numpy, fmt="%s",delimiter=",")
            zipf = zipfile.ZipFile(f'{infer_result}.zip','w', zipfile.ZIP_DEFLATED)
            for item in infer:
                zipf.write(f'{infer_result}/result/{item[5]}')
            zipf.write(f'{infer_result}/result.txt')
            zipf.close()
        
        thread = threading.Thread(target=process_video,args=(video.filename,))
        thread.start()
        #return 
        '''
        return send_file(f'{infer_result}.zip',
                mimetype = 'zip',
                attachment_filename= f'{infer_result}.zip',
                as_attachment = True)
        '''
    except Exception as e:
        response = jsonify({'status':400,'message': str(e)})
        return response, 400
    return "video received"
    #return jsonify({'result':infer})


@app.route('/get_video_status/<filename>', methods=['GET'])
def get_video_status(filename):
    file_zip = f'{filename}_result.zip'
    print("file_zip:",file_zip)
    print("boolean:",os.path.exists(file_zip))
    if os.path.exists(file_zip):
        with open(file_zip, 'rb') as f:
            data = f.readlines()
        os.remove(file_zip)
        return Response(data, headers={
            'Content-Type': 'application/zip',
            'Content-Disposition': 'attachment; filename=%s;' % file_zip
            })
        #archive = zipfile.ZipFile(file_zip, 'r')
        #print("archive:",archive)
        #print("archiveType:",type(archive))
        #return "complete"
    else:
        return "still processing",404

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logging.error(e)
