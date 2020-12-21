## What is this

This is the code repository of an agent to transform and synchronize video streaming data and video structuring data running on [edge device](https://en.wikipedia.org/wiki/Edge_computing).
The code name of this component is [Riverrun](https://gameofthrones.fandom.com/wiki/Riverrun).

This agent includes four correlative serverless applications build in [AWS Serverless Application Model](https://aws.amazon.com/serverless/sam/), each one is developed as a [AWS Lambda](https://aws.amazon.com/lambda/) [Function](https://github.com/zhiyanliu/riverrun/blob/master/template.yaml) by Python (python3.7 runtime).

These applications can be deployed together on the same edge device or be distributed to the different device as deployment architecture needs, e.g. deployment on limited hardware resources or affect by the division of device capability.
They also can be fully or partially deployed based on customer's requirement.

The performance of this project has been tuned for resource-limited hardware as well, it has been deployed on [Dragonboard 410c](https://developer.qualcomm.com/hardware/dragonboard-410c) by [AWS IoT Greengrass](https://aws.amazon.com/greengrass/) service in a real customer case.

Mainly, and currently, Riverrun provides four functions:

1. `MetadataFrameEmitter`: Video streaming data collecting and transmitting. Support to collect video packet from socket API or customer's SDK, to transmit by UDP and TCP protocols in Publish/Subscribe and Request/Response modes.
2. `VideoEmitter`: Video structuring data collecting and transmitting. Support to collect video frame metadata from socket API or customer's SDK, to transmit by TCP protocol in Publish/Subscribe and Request/Response modes.
3. `VideoProcessor`: Video streaming data and structuring data transform and synchronize. Support two synchronization policies according to the video structuring QoS, and structuring data throttling based on hardware resource limit to reduce video streaming delay.
4. `VideoStreamer`: Decoding video streaming and structuring data to log and dump H.264 packets, used for functional and performance testing or additional data handling in future.

## Why develop it

The data transformation and synchronization for video streaming and structuring data on edge device is a common requirement in modern computer vision related project. Currently our SA and developer needs to implement, test and tuning such similar functions for different project, and beside the duplicated workload, in most time the deliverable is not easy to develop quickly especially in the scenario about streaming data handling on resource-limited hardware.

To easy the developer and our SA to deliver this kind of project, I generalized and polished our video streaming data and structuring data transformation and synchronization project to make it for common usage, to accelerate the PoC, prototyping case delivery.

>> **Note:**
>>
>> This project is truly under continuative develop stage, I'd like to collect the feedback and include the enhancement in follow-up release to share them with all users.
>>
>> **DISCLAIMER: This project is NOT intended for a production environment, and USE AT OWN RISK!**

## Limit

This project does not work for you if:

* You would not like to use AWS Lambda server to manage your functions.
* You would not like to use AWS Serverless Application Model (SAM) to organize your software architecture.
* You would not like to involve Python lang to your technical stack.
* You do not have a credential to access WW (non-China) AWS region.
* Your AWS account user has not right to fully access Amazon S3, AWS Lambda and AWS CloudFormation services.
* You do not have a host runs MacOS, Ubuntu or Windows system, to install and run AWS SAM CLI.

>>**Preferred software version:**
>>
>> - AWS SAM CLI: 0.34.0, or above

## How to deploy

1. ``git clone git@git.awsrun.com:rp/riverrun.git``
2. ``cd riverrun``
3. Create a S3 bucket to save Lambda function package. E.g. using AWS CLI: ``aws s3 mb s3://<YOUR S3 BUCKET NAME>``
4. **When using Horizon SDK to receive video streaming and structuring data only:** Hot-fix AWS SAM CLI to include `so` file in the Lambda function package before the [issue](https://github.com/awslabs/aws-sam-cli/issues/1360) is fixed, because Horizon SDK is released as a `hobotx2.so` file.
   - Open your local SAM CLI file ``aws_lambda_builders/workflows/python_pip/workflow.py``. For example, `brew` installed this file at `/usr/local/Cellar/aws-sam-cli/0.34.0/libexec/lib/python3.7/site-packages/aws_lambda_builders/workflows/python_pip/workflow.py` on my Mac. Also, online version at [here](``https://github.com/awslabs/aws-lambda-builders/blob/develop/aws_lambda_builders/workflows/python_pip/workflow.py#L27``).
   - Located to line #27, this code line is ``"*.pyc", "__pycache__", "*.so",``.
   - Replace this code line to ``"*.pyc", "__pycache__",``.
5. ``sam build --template template.yaml --build-dir pkg/build``
6. ``sam package --template-file pkg/build/template.yaml --output-template-file pkg/build/packaged-template.yaml --s3-bucket <YOUR S3 BUCKET NAME>``
7. ``sam deploy --template-file pkg/build/packaged-template.yaml --stack-name --capabilities CAPABILITY_IAM <YOUR STACK NAME>``

>> **Note:**
>>
>> - If you are using Windows system, you need to update the path in above `sam` commands to use Windows style path separator.
>> - You need not to execute above step \#4 when you intend to use socket API to receive video streaming and structuring data instead of using Horizon SDK.

## How to config

### Lambda supported environment variables

- Function `MetadataFrameEmitter`

    |Environment variable name             |Description                                                                                                                                                                                                                      |Type                           |Available options          |Default value|
    |--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|---------------------------|-------------|
    |METADATA_FRAME_SERVER_IP              |The name or IP of the host function `VideoProcessor` running on as the target address to send video metadata frame (video structuring data for each video frame) to.                                                             |String (Hostname or IP address)|N/A                        |N/A          |
    |METADATA_FRAME_SERVER_PORT            |The port of the host function `VideoProcessor` running on as the target port to send video metadata frame to. Need to match to the setting of the option `METADATA_FRAME_SERVER_PORT` of function `VideoProcessor`.              |Integer (0-65535)              |N/A                        |9528         |
    |METADATA_FRAME_EMIT_TYPE              |The type of video metadata frame transmission mode. Need to match to the setting of the option `METADATA_FRAME_TAKE_TYPE` of function `VideoProcessor`.                                                                          |String (Option)                |`PUB`, `REQ`               |`PUB`        |
    |METADATA_FRAME_REQUEST_RELY_TIMEOUT_MS|The timeout of receiving `ACK` packet from function `VideoProcessor`, in millisecond unit. Only when option `METADATA_FRAME_EMIT_TYPE` sets to `REQ`.                                                                            |Integer (>0)                   |N/A                        |500          |
    |METADATA_FRAME_PUBLISH_TOPIC          |The topic name used for publishing video metadata frame out. Only when option `METADATA_FRAME_EMIT_TYPE` sets to `PUB`. Need to match to the setting of the option `METADATA_FRAME_SUBSCRIBE_TOPIC` of function `VideoProcessor`.|String                         |N/A                        |md           |
    |METADATA_FRAME_INPUT_TYPE             |The type of video metadata frame collection mode. Option `HORIZON_SDK` means to read video metadata frame from Horizon SDK, option `NET_SOCKET` means to receive video metadata frame from socket API.                           |String (Option)                |`HORIZON_SDK`, `NET_SOCKET`|`NET_SOCKET` |
    |METADATA_FRAME_NET_SOCKET_SERVER_PORT |The port socket API server listen on. Only when option `METADATA_FRAME_INPUT_TYPE` sets to `NET_SOCKET`.                                                                                                                         |Integer (0-65535)              |N/A                        |9525         |

- Function `VideoEmitter`

    |Environment variable name              |Description                                                                                                                                                                                                                         |Type                           |Available options          |Default value|
    |---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|---------------------------|-------------|
    |VIDEO_STREAM_SERVER_IP                 |The name or IP of the host function `VideoProcessor` running on as the target address to send video packet (video streaming data) to.                                                                                               |String (Hostname or IP address)|N/A                        |N/A          |
    |VIDEO_STREAM_SERVER_PORT               |The port of the host function `VideoProcessor` running on as the target port to send video packet to. Need to match to the setting of the option `VIDEO_STREAM_SERVER_PORT` of function `VideoProcessor`.                           |Integer (0-65535)              |N/A                        |9530         |
    |VIDEO_STREAM_EMIT_TYPE                 |The type of video packet transmission mode. Need to match to the setting of the option `VIDEO_STREAM_TAKE_TYPE` of function `VideoProcessor`.                                                                                       |String (Option)                |`PUB`, `REQ`, `UDP`        |`PUB`        |
    |VIDEO_STREAM_REQUEST_RELY_TIMEOUT_MS   |The timeout of receiving `ACK` packet from function `VideoProcessor`, in millisecond unit. Only when option `VIDEO_STREAM_EMIT_TYPE` sets to `REQ`.                                                                                 |Integer (>0)                   |N/A                        |500          |
    |VIDEO_STREAM_PUBLISH_TOPIC             |The topic name used for publishing video packet out. Only when option `VIDEO_STREAM_EMIT_TYPE` sets to `PUB`. Need to match to the setting of the option `VIDEO_STREAM_SUBSCRIBE_TOPIC` of function `VideoProcessor`.               |String                         |N/A                        |rtp          |
    |VIDEO_RTP_PACKET_INPUT_TYPE            |The type of video packet collection mode. Option `HORIZON_SDK` means to read video packet from Horizon SDK, option `NET_SOCKET` means to receive video packet from socket API.                                                      |String (Option)                |`HORIZON_SDK`, `NET_SOCKET`|`NET_SOCKET` |
    |VIDEO_RTP_PACKET_SHM_FILENAME          |The share memory file name located in directory `/dev/shm` which stores the video packet writes by `Horizon` under layer software (in short, it is gst-launch-1.0, the pipeline is `v4l2src ! v4l2h264enc ! rtph264pay ! fakesink`).|String                         |N/A                        |foo_30M      |
    |VIDEO_RTP_PACKET_NET_SOCKET_SERVER_PORT|The port socket API server listen on. Only when option `VIDEO_RTP_PACKET_INPUT_TYPE` sets to `NET_SOCKET`.                                                                                                                          |Integer (0-65535)              |N/A                        |9526         |

- Function `VideoProcessor`

    |Environment variable name                  |Description                                                                                                                                                                                                                                                       |Type                           |Available options     |Default value|
    |-------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|----------------------|-------------|
    |METADATA_FRAME_SERVER_PORT                 |The port video metadata frame server listen on. Need to match to the setting of the option `METADATA_FRAME_SERVER_PORT` of function `MetadataFrameEmitter`.                                                                                                       |Integer (0-65535)              |N/A                   |9528         |
    |METADATA_FRAME_TAKE_TYPE                   |The type of video metadata frame transmission mode. Need to match to the setting of the option `METADATA_FRAME_EMIT_TYPE` of function `MetadataFrameEmitter`.                                                                                                     |String (Option)                |`SUB`, `REP`          |`SUB`        |
    |METADATA_FRAME_SUBSCRIBE_TOPIC             |The topic name used for subscribing video metadata frame in. Only when option `METADATA_FRAME_TAKE_TYPE` sets to `SUB`. Need to match to the setting of the option `METADATA_FRAME_PUBLISH_TOPIC` of function `MetadataFrameEmitter`.                             |String                         |N/A                   |md           |
    |METADATA_FRAME_THROTTLE_TOLERATE_COUNT     |The threshold to trigger flow control on video metadata frame retrieving. It is used for reducing video streaming delay caused by synchronization waiting on the slow metadata frame handling.                                                                    |Integer (>-1)                  |N/A                   |0            |
    |VIDEO_STREAM_SERVER_PORT                   |The port video packet server listen on. Need to match to the setting of the option `VIDEO_STREAM_SERVER_PORT` function `VideoEmitter`.                                                                                                                            |Integer (0-65535)              |N/A                   |9530         |
    |VIDEO_STREAM_TAKE_TYPE                     |The type of video packet transmission mode. Need to match to the setting of the option `VIDEO_STREAM_EMIT_TYPE` of function `VideoEmitter`.                                                                                                                       |String (Option)                |`SUB`, `REP`, `UDP`   |`SUB`        |
    |VIDEO_STREAM_SUBSCRIBE_TOPIC               |The topic name used for subscribing video packet in. Only when option `VIDEO_STREAM_TAKE_TYPE` sets to `SUB`.  Need to match to the setting of the option `VIDEO_STREAM_PUBLISH_TOPIC` of function `VideoEmitter`.                                                |String                         |N/A                   |rtp          |
    |SYNC_PACKET_POLICY_TYPE                    |The type of video packet and video metadata frame synchronization policy.                                                                                                                                                                                         |String (Option)                |`ONE_SHOT`, `DEADLINE`|`ONE_SHOT`   |
    |SYNC_PACKET_POLICY_QUEUE_SIZE              |The queue depth used for video packet and video metadata frame synchronization.                                                                                                                                                                                   |Integer (>0)                   |N/A                   |15           |
    |SYNC_PACKET_POLICY_SEND_METADATA_FRAME_ONCE|Option `No` means to send multiple same video metadata frames with every RTP fragmentation units of the video frame in the synchronization packet. Option `Yes` means only send one video metadata frame with the first RTP fragmentation unit of the video frame.|String (Boolean)               |`Yes`, `No`           |`Yes`        |
    |SYNC_PACKET_SERVER_IP                      |The name or IP of the host function `VideoStreamer` running on as the target address to send synchronization packet to.                                                                                                                                           |String (Hostname or IP address)|N/A                   |N/A          |
    |SYNC_PACKET_SERVER_PORT                    |The port of the host function `VideoStreamer` running on as the target address to send synchronization packet to.  Need to match to the setting of the option `SYNC_PACKET_SERVER_PORT` of function `VideoStreamer`.                                              |Integer (0-65535)              |N/A                   |9532         |
    |SYNC_PACKET_SERVER_HEARTBEAT_TIMEOUT_SEC   |The timeout of retrieving heartbeat from function `VideoProcessor`, in second unit. After timeout a warning message will be logged.                                                                                                                               |Integer (>0)                   |N/A                   |30           |

- Function `VideoStreamer`

    |Environment variable name                |Description                                                                                                                                                                                                                                     |Type              |Available options|Default value                             |
    |-----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|-----------------|------------------------------------------|
    |SYNC_PACKET_SERVER_PORT                  |The port video streamer server listen on. Need to match to the setting of the option `SYNC_PACKET_SERVER_PORT` of function `VideoProcessor`.                                                                                                    |Integer (0-65535) |N/A              |9532                                      |
    |SYNC_PACKET_SERVER_HEARTBEAT_INTERVAL_SEC|The interval to send heartbeat to function `VideoProcessor`, in second unit. Also, after double of the value time, the idle connection will be closed positively.                                                                               |Integer (>0)      |N/A              |20                                        |
    |METADATA_FRAME_FILE_PATH                 |The file used for dumping the data about every received video metadata frames. The video metadata frame socket API format will be used: `<TIMESTAMP(int(4), big-endian)><METADATA_LENGTH(int(4), big-endian)><METADATA(char[METADATA_LENGTH])>`.|String (*NIX Path)|N/A              |/tmp/riverrun-streamer/metadata_frame.dump|
    |RTP_PACKET_FILE_SAVE_PATH                |The file used for dumping the data about every received video packets. The video packet socket API format will be used: `<RTP_LENGTH(int(4), big-endian)><RTP(char[RTP_LENGTH])>`.                                                              |String (*NIX Path)|N/A              |/tmp/riverrun-streamer/video_rtp.dump     |
    |VIDEO_PACKET_FILE_SAVE_PATH              |The file used for dumping the data about every received video packets with additional timestamp. Format: `<TIMESTAMP(int(4), big-endian)><RTP_LENGTH(int(4), big-endian)><RTP(char[RTP_LENGTH])>`.                                              |String (*NIX Path)|N/A              |/tmp/riverrun-streamer/video_packet.dump  |

### Local resource of Greengrass Core

- Resource `VIDEO_RTP_PACKET_INPUT_DEVICE`

    |Resource type|Source path       |Destination path  |Lambda function affiliations|Group owner file access permission                                               |Note                                                                                                                             |
    |-------------|------------------|------------------|----------------------------|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
    |`Volume`     |`/dev/shm/foo_30M`|`/dev/shm/foo_30M`|`VideoEmitter`              |Automatically add OS group permissions of the Linux group that owns the resource.|The file name in the path needs to match to the setting of the option `VIDEO_RTP_PACKET_SHM_FILENAME` of function `VideoEmitter`.|

    >> **Note:**
    >>
    >> This local resource configuration is needed only when you are setting option `VIDEO_RTP_PACKET_INPUT_TYPE` to value `HORIZON_SDK` for function `VideoEmitter`. 

### Dependencies on edge device

- ``sudo apt-get update``
- ``apt install -y unzip python3.7 python3.7-dev python3-pip python3-apt build-essential``
- ``sudo ln -sf /usr/bin/python3.7 /usr/bin/python3``
- ``sudo -H pip3 install pyzmq --install-option='--zmq=bundled'``

## Key TODO plan:

- [ ] Move library `pyzmq` import into correlative class scope, instead of a global dependency.
- [ ] Decode H.264 NAL to video frame.
- [ ] Implement picture saver to save video frame to picture at local filesystem in PNG format.
- [ ] Implement Websocket server to expose video frame to picture in PNG format.

## Contributor

* Zhi Yan Liu, [liuzhiya@amazon.com](mailto:liuzhiya@amazon.com)
* You. Welcome any feedback and issue report, further more, idea and code contribution are highly encouraged.
