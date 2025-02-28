Title: Create transcript — ElevenLabs Documentation

URL Source: https://elevenlabs.io/docs/api-reference/speech-to-text/convert

Markdown Content:
Search
/
Community
Blog
Help Center
Pricing
Sign up
Docs
Conversational AI
API reference
API REFERENCE
Introduction
Authentication
Streaming
Websocket
ENDPOINTS
Text to Speech
Speech to Text
POST
Create transcript
Voice Changer
Sound Effects
Audio Isolation
Text to Voice
Dubbing
Audio Native
Voices
ADMINISTRATION
History
Models
Studio
Pronunciation Dictionary
Samples
Usage
User
Voice Library
Workspace
CONVERSATIONAL AI
Agents
Conversations
Knowledge Base
Tools
Phone Numbers
Widget
Workspace
LEGACY
Voice Generation (Deprecated)
Projects
ENDPOINTS
Speech to Text
Create transcript
POST
https://api.elevenlabs.io
/v1/speech-to-text

Transcribe an audio or video file.

Request
This endpoint expects a multipart form containing a file.
model_id
string
Required

The ID of the model to use for transcription, currently only ‘scribe_v1’ is available.

file
file
Required
language_code
string
Optional

An ISO-639-1 or ISO-639-3 language_code corresponding to the language of the audio file. Can sometimes improve transcription performance if known beforehand. Defaults to null, in this case the language is predicted automatically.

tag_audio_events
boolean
Optional
Defaults to true

Whether to tag audio events like (laughter), (footsteps), etc. in the transcription.

num_speakers
integer
Optional
>=1
<=32

The maximum amount of speakers talking in the uploaded file. Can help with predicting who speaks when. The maximum amount of speakers that can be predicted is 32. Defaults to null, in this case the amount of speakers is set to the maximum value the model supports.

timestamps_granularity
enum
Optional
Defaults to word

The granularity of the timestamps in the transcription. ‘word’ provides word-level timestamps and ‘character’ provides character-level timestamps per word.

Allowed values:
none
word
character
diarize
boolean
Optional
Defaults to false

Whether to annotate which speaker is currently talking in the uploaded file. Enabling this will limit the maximum duration of your inputs to 8 minutes.

Response

Successful Response

language_code
string

The detected language code (e.g. ‘eng’ for English).

language_probability
double

The confidence score of the language detection (0 to 1).

text
string

The raw text of the transcription.

words
list of objects

List of words with their timing information.

Show 6 properties
Errors
422
Speech to Text Convert Request Unprocessable Entity Error
POST
/v1/speech-to-text
cURL
1	curl -X POST https://api.elevenlabs.io/v1/speech-to-text \
2	     -H "xi-api-key: <apiKey>" \
3	     -H "Content-Type: multipart/form-data" \
4	     -F model_id="model_id" \
5	     -F file=@<file1>
Try it
200
Successful
1	{
2	  "language_code": "en",
3	  "language_probability": 0.98,
4	  "text": "Hello world!",
5	  "words": [
6	    {
7	      "text": "Hello",
8	      "type": "word",
9	      "start": 0,
10	      "end": 0.5,
11	      "speaker_id": "speaker_1",
12	      "characters": [
13	        {
14	          "text": "text",
15	          "start": 0,
16	          "end": 0.1
17	        }
18	      ]
19	    },
20	    {
21	      "text": " ",
22	      "type": "spacing",
23	      "start": 0.5,
24	      "end": 0.5,
25	      "speaker_id": "speaker_1",
26	      "characters": [
27	        {
28	          "text": "text",
29	          "start": 0,
30	          "end": 0.1
31	        }
32	      ]
33	    },
34	    {
35	      "text": "world!",
36	      "type": "word",
37	      "start": 0.5,
38	      "end": 1.2,
39	      "speaker_id": "speaker_1",
40	      "characters": [
41	        {
42	          "text": "text",
43	          "start": 0,
44	          "end": 0.1
45	        }
46	      ]
47	    }
48	  ]
49	}
Built with
