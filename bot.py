{\rtf1\ansi\ansicpg1251\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import requests\
import logging\
import numpy as np\
import talib\
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup\
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, filters\
import numpy.random  # \uc0\u1048 \u1084 \u1087 \u1086 \u1088 \u1090  \u1076 \u1083 \u1103  \u1075 \u1077 \u1085 \u1077 \u1088 \u1072 \u1094 \u1080 \u1080  \u1085 \u1077 \u1073 \u1086 \u1083 \u1100 \u1096 \u1080 \u1093  \u1089 \u1083 \u1091 \u1095 \u1072 \u1081 \u1085 \u1099 \u1093  \u1095 \u1080 \u1089 \u1077 \u1083 \
import sqlite3  # \uc0\u1048 \u1084 \u1087 \u1086 \u1088 \u1090  \u1076 \u1083 \u1103  \u1088 \u1072 \u1073 \u1086 \u1090 \u1099  \u1089  SQLite\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  1: \u1053 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1072  \u1080  \u1048 \u1085 \u1080 \u1094 \u1080 \u1072 \u1083 \u1080 \u1079 \u1072 \u1094 \u1080 \u1103 \
#                       \uc0\u1048 \u1084 \u1087 \u1086 \u1088 \u1090 \u1099 , \u1083 \u1086 \u1075 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1080 \u1077 , \u1103 \u1079 \u1099 \u1082 \u1086 \u1074 \u1099 \u1077  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1080 \
# ======================================================================\
\
# --- \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1072  \u1083 \u1086 \u1075 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1080 \u1103  ---\
logging.basicConfig(\
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",\
    level=logging.INFO,\
)\
logger = logging.getLogger(__name__)\
\
# --- \uc0\u1057 \u1083 \u1086 \u1074 \u1072 \u1088 \u1080  \u1089  \u1090 \u1077 \u1082 \u1089 \u1090 \u1072 \u1084 \u1080  \u1085 \u1072  \u1088 \u1072 \u1079 \u1085 \u1099 \u1093  \u1103 \u1079 \u1099 \u1082 \u1072 \u1093  ---\
TEXTS = \{\
    'ru': \{\
        'start_message': "\uc0\u55357 \u56522  \u1042 \u1099 \u1073 \u1077 \u1088 \u1080 \u1090 \u1077  \u1076 \u1077 \u1081 \u1089 \u1090 \u1074 \u1080 \u1077  \u1080 \u1083 \u1080  \u1074 \u1074 \u1077 \u1076 \u1080 \u1090 \u1077  \u1090 \u1080 \u1082 \u1077 \u1088  \u1080 \u1083 \u1080  \u1079 \u1072 \u1087 \u1088 \u1086 \u1089  (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 : BTC, 12 SUI USDT, 10 STRK TWT):",\
        'help_message_header': "\uc0\u55357 \u56481  **\u1050 \u1072 \u1082  \u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1100  \u1073 \u1086 \u1090 \u1072 :**\\n\\n",\
        'help_message_calculation_header': "**\uc0\u1044 \u1083 \u1103  \u1088 \u1072 \u1089 \u1095 \u1077 \u1090 \u1072  \u1089 \u1090 \u1086 \u1080 \u1084 \u1086 \u1089 \u1090 \u1080 :**\\n",\
        'help_message_calculation_text': "\uc0\u1042 \u1074 \u1077 \u1076 \u1080 \u1090 \u1077  \u1082 \u1086 \u1083 \u1080 \u1095 \u1077 \u1089 \u1090 \u1074 \u1086  \u1080  \u1087 \u1072 \u1088 \u1091  \u1084 \u1086 \u1085 \u1077 \u1090 , \u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 : `12 SUI USDT` \u1080 \u1083 \u1080  `0.5 ETH BTC` \u1080 \u1083 \u1080  `10 STRK TWT`.\\n"\
        "- \uc0\u1041 \u1086 \u1090  \u1074 \u1077 \u1088 \u1085 \u1077 \u1090  \u1089 \u1090 \u1086 \u1080 \u1084 \u1086 \u1089 \u1090 \u1100  \u1091 \u1082 \u1072 \u1079 \u1072 \u1085 \u1085 \u1086 \u1075 \u1086  \u1082 \u1086 \u1083 \u1080 \u1095 \u1077 \u1089 \u1090 \u1074 \u1072  \u1087 \u1077 \u1088 \u1074 \u1086 \u1081  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  \u1074 \u1086  \u1074 \u1090 \u1086 \u1088 \u1086 \u1081  \u1074 \u1072 \u1083 \u1102 \u1090 \u1077 .\\n"\
        "- \uc0\u1044 \u1083 \u1103  USDT \u1087 \u1072 \u1088 , \u1094 \u1077 \u1085 \u1072  \u1073 \u1091 \u1076 \u1077 \u1090  \u1087 \u1086 \u1082 \u1072 \u1079 \u1072 \u1085 \u1072  \u1074  \u1076 \u1086 \u1083 \u1083 \u1072 \u1088 \u1072 \u1093  ($).\\n"\
        "- \uc0\u1044 \u1083 \u1103  \u1082 \u1088 \u1080 \u1087 \u1090 \u1086 -\u1082 \u1088 \u1080 \u1087 \u1090 \u1086  \u1087 \u1072 \u1088  (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 , ETH BTC, STRK TWT), \u1094 \u1077 \u1085 \u1072  \u1073 \u1091 \u1076 \u1077 \u1090  \u1087 \u1086 \u1082 \u1072 \u1079 \u1072 \u1085 \u1072  \u1074 \u1086  \u1074 \u1090 \u1086 \u1088 \u1086 \u1081  \u1082 \u1088 \u1080 \u1087 \u1090 \u1086 \u1074 \u1072 \u1083 \u1102 \u1090 \u1077 .\\n\\n",\
        'help_message_calculation_examples_header': "**\uc0\u1055 \u1088 \u1080 \u1084 \u1077 \u1088 \u1099  \u1079 \u1072 \u1087 \u1088 \u1086 \u1089 \u1086 \u1074  \u1076 \u1083 \u1103  \u1088 \u1072 \u1089 \u1095 \u1077 \u1090 \u1072 :**\\n",\
        'help_message_calculation_examples_text': "- `12 SUI USDT` -  \uc0\u1091 \u1079 \u1085 \u1072 \u1090 \u1100  \u1089 \u1090 \u1086 \u1080 \u1084 \u1086 \u1089 \u1090 \u1100  12 SUI \u1074  \u1076 \u1086 \u1083 \u1083 \u1072 \u1088 \u1072 \u1093  \u1057 \u1064 \u1040 .\\n"\
        "- `0.5 ETH BTC` - \uc0\u1091 \u1079 \u1085 \u1072 \u1090 \u1100  \u1089 \u1090 \u1086 \u1080 \u1084 \u1086 \u1089 \u1090 \u1100  0.5 ETH \u1074  BTC.\\n"\
        "- `10 STRK TWT` - \uc0\u1091 \u1079 \u1085 \u1072 \u1090 \u1100  \u1089 \u1090 \u1086 \u1080 \u1084 \u1086 \u1089 \u1090 \u1100  10 STRK TWT.\\n\\n",\
        'help_message_technical_analysis_header': "**\uc0\u1044 \u1083 \u1103  \u1087 \u1086 \u1083 \u1091 \u1095 \u1077 \u1085 \u1080 \u1103  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1086 \u1075 \u1086  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079 \u1072  (\u1082 \u1072 \u1083 \u1100 \u1082 \u1091 \u1083 \u1103 \u1090 \u1086 \u1088 ) \u1089  \u1088 \u1072 \u1079 \u1085 \u1099 \u1084 \u1080  \u1090 \u1072 \u1081 \u1084 \u1092 \u1088 \u1077 \u1081 \u1084 \u1072 \u1084 \u1080 :**\\n",\
        'help_message_technical_analysis_text': "\uc0\u1055 \u1088 \u1086 \u1089 \u1090 \u1086  \u1074 \u1074 \u1077 \u1076 \u1080 \u1090 \u1077  \u1090 \u1080 \u1082 \u1077 \u1088  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 , `BTC`, `ETH`, `SUI`). \u1041 \u1086 \u1090  \u1087 \u1086 \u1082 \u1072 \u1078 \u1077 \u1090 :\\n"\
                                                  "- \uc0\u1058 \u1077 \u1082 \u1091 \u1097 \u1091 \u1102  \u1094 \u1077 \u1085 \u1091  (\u1074 \u1089 \u1077 \u1075 \u1076 \u1072 )\\n"\
                                                  "- \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1080 \u1077  \u1094 \u1077 \u1085 \u1099  \u1079 \u1072  \u1074 \u1099 \u1073 \u1088 \u1072 \u1085 \u1085 \u1099 \u1081  \u1090 \u1072 \u1081 \u1084 \u1092 \u1088 \u1077 \u1081 \u1084  \u1074  \u1087 \u1088 \u1086 \u1094 \u1077 \u1085 \u1090 \u1072 \u1093 \\n"\
                                                  "- \uc0\u1058 \u1086 \u1088 \u1075 \u1086 \u1074 \u1099 \u1081  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083  \u1080  \u1090 \u1088 \u1077 \u1085 \u1076  \u1076 \u1083 \u1103  \u1074 \u1099 \u1073 \u1088 \u1072 \u1085 \u1085 \u1086 \u1075 \u1086  \u1090 \u1072 \u1081 \u1084 \u1092 \u1088 \u1077 \u1081 \u1084 \u1072 \\n"\
                                                  "- \uc0\u1050 \u1085 \u1086 \u1087 \u1082 \u1080  \u1076 \u1083 \u1103  \u1087 \u1077 \u1088 \u1077 \u1082 \u1083 \u1102 \u1095 \u1077 \u1085 \u1080 \u1103  \u1085 \u1072  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1080 \u1081  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079  \u1076 \u1083 \u1103  \u1090 \u1072 \u1081 \u1084 \u1092 \u1088 \u1077 \u1081 \u1084 \u1086 \u1074 : 1\u1095 , 4\u1095 , 12\u1095 , \u1053 \u1072 \u1079 \u1072 \u1076 \\n"\
                                                  "**\uc0\u1042 \u1099  \u1084 \u1086 \u1078 \u1077 \u1090 \u1077  \u1087 \u1077 \u1088 \u1077 \u1082 \u1083 \u1102 \u1095 \u1080 \u1090 \u1100  \u1103 \u1079 \u1099 \u1082  \u1073 \u1086 \u1090 \u1072  \u1085 \u1072  \u1072 \u1085 \u1075 \u1083 \u1080 \u1081 \u1089 \u1082 \u1080 \u1081  \u1080 \u1083 \u1080  \u1088 \u1091 \u1089 \u1089 \u1082 \u1080 \u1081 , \u1085 \u1072 \u1078 \u1072 \u1074  \u1089 \u1086 \u1086 \u1090 \u1074 \u1077 \u1090 \u1089 \u1090 \u1074 \u1091 \u1102 \u1097 \u1080 \u1077  \u1082 \u1085 \u1086 \u1087 \u1082 \u1080  \u1085 \u1080 \u1078 \u1077 .**\\n\\n",\
        'help_message_technical_analysis_features_header': "**\uc0\u1055 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1080 \u1074 \u1072 \u1077 \u1084 \u1099 \u1077  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1080  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1086 \u1075 \u1086  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079 \u1072 :**\\n",\
        'help_message_technical_analysis_features_text': "- RSI (\uc0\u1048 \u1085 \u1076 \u1077 \u1082 \u1089  \u1086 \u1090 \u1085 \u1086 \u1089 \u1080 \u1090 \u1077 \u1083 \u1100 \u1085 \u1086 \u1081  \u1089 \u1080 \u1083 \u1099 )\\n"\
        "- MACD (\uc0\u1057 \u1093 \u1086 \u1078 \u1076 \u1077 \u1085 \u1080 \u1077 /\u1056 \u1072 \u1089 \u1093 \u1086 \u1078 \u1076 \u1077 \u1085 \u1080 \u1077  \u1057 \u1082 \u1086 \u1083 \u1100 \u1079 \u1103 \u1097 \u1080 \u1093  \u1057 \u1088 \u1077 \u1076 \u1085 \u1080 \u1093 )\\n"\
        # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  30 \u1080  100\
        "- EMA (\uc0\u1069 \u1082 \u1089 \u1087 \u1086 \u1085 \u1077 \u1085 \u1094 \u1080 \u1072 \u1083 \u1100 \u1085 \u1072 \u1103  \u1089 \u1082 \u1086 \u1083 \u1100 \u1079 \u1103 \u1097 \u1072 \u1103  \u1089 \u1088 \u1077 \u1076 \u1085 \u1103 \u1103 ) - 30 \u1080  100 \u1087 \u1077 \u1088 \u1080 \u1086 \u1076 \u1086 \u1074 \\n"\
        "- Bollinger Bands (\uc0\u1055 \u1086 \u1083 \u1086 \u1089 \u1099  \u1041 \u1086 \u1083 \u1083 \u1080 \u1085 \u1076 \u1078 \u1077 \u1088 \u1072 )\\n"\
        "- Stochastic Oscillator (\uc0\u1057 \u1090 \u1086 \u1093 \u1072 \u1089 \u1090 \u1080 \u1095 \u1077 \u1089 \u1082 \u1080 \u1081  \u1086 \u1089 \u1094 \u1080 \u1083 \u1083 \u1103 \u1090 \u1086 \u1088 )\\n"\
        "- SMA (\uc0\u1055 \u1088 \u1086 \u1089 \u1090 \u1072 \u1103  \u1089 \u1082 \u1086 \u1083 \u1100 \u1079 \u1103 \u1097 \u1072 \u1103  \u1089 \u1088 \u1077 \u1076 \u1085 \u1103 \u1103 ) - 20 \u1080  50 \u1087 \u1077 \u1088 \u1080 \u1086 \u1076 \u1086 \u1074 \\n"\
        "- Parabolic SAR (\uc0\u1055 \u1072 \u1088 \u1072 \u1073 \u1086 \u1083 \u1080 \u1095 \u1077 \u1089 \u1082 \u1072 \u1103  \u1089 \u1080 \u1089 \u1090 \u1077 \u1084 \u1072  SAR)\\n"\
        "- ADX (\uc0\u1048 \u1085 \u1076 \u1077 \u1082 \u1089  \u1085 \u1072 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085 \u1085 \u1086 \u1075 \u1086  \u1076 \u1074 \u1080 \u1078 \u1077 \u1085 \u1080 \u1103 )\\n"\
        "- Ichimoku Cloud (\uc0\u1054 \u1073 \u1083 \u1072 \u1082 \u1086  \u1048 \u1096 \u1080 \u1084 \u1086 \u1082 \u1091 )\\n"\
        "- Williams %R (\uc0\u1055 \u1088 \u1086 \u1094 \u1077 \u1085 \u1090 \u1085 \u1099 \u1081  \u1076 \u1080 \u1072 \u1087 \u1072 \u1079 \u1086 \u1085  \u1042 \u1080 \u1083 \u1100 \u1103 \u1084 \u1089 \u1072 )\\n"\
        "- **OBV (On Balance Volume) - \uc0\u1041 \u1072 \u1083 \u1072 \u1085 \u1089 \u1086 \u1074 \u1099 \u1081  \u1086 \u1073 \u1098 \u1077 \u1084 **\\n"\
        "- \uc0\u1059 \u1088 \u1086 \u1074 \u1085 \u1080  \u1087 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1082 \u1080  \u1080  \u1089 \u1086 \u1087 \u1088 \u1086 \u1090 \u1080 \u1074 \u1083 \u1077 \u1085 \u1080 \u1103 \\n"\
        "- \uc0\u1059 \u1088 \u1086 \u1074 \u1085 \u1080  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080 \\n",\
\
\
\
        'help_message_other_functions_header': "**\uc0\u1044 \u1088 \u1091 \u1075 \u1080 \u1077  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1080 :**\\n",\
        'help_message_other_functions_text': "- \uc0\u1056 \u1072 \u1079 \u1076 \u1077 \u1083  '\u1058 \u1086 \u1087  10 \u1088 \u1086 \u1089 \u1090  \u55357 \u56960 ' \u1080  '\u1058 \u1086 \u1087  10 \u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103  \u55357 \u56521 ' \u1087 \u1086 \u1082 \u1072 \u1079 \u1099 \u1074 \u1072 \u1077 \u1090  \u1083 \u1080 \u1076 \u1077 \u1088 \u1086 \u1074  \u1088 \u1086 \u1089 \u1090 \u1072  \u1080  \u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103  \u1085 \u1072  Binance.\\n"\
                                               "- \uc0\u1056 \u1072 \u1079 \u1076 \u1077 \u1083  '\u1055 \u1086 \u1084 \u1086 \u1097 \u1100 ' - \u1090 \u1077 \u1082 \u1091 \u1097 \u1072 \u1103  \u1089 \u1087 \u1088 \u1072 \u1074 \u1082 \u1072 .\\n"\
                                               "- \uc0\u1056 \u1072 \u1079 \u1076 \u1077 \u1083  'Donat' - \u1076 \u1083 \u1103  \u1087 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1082 \u1080  \u1088 \u1072 \u1079 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082 \u1072 .\\n"\
                                               "- \uc0\u1053 \u1045  \u1060 \u1048 \u1053 \u1040 \u1053 \u1057 \u1054 \u1042 \u1040 \u1071  \u1056 \u1045 \u1050 \u1054 \u1052 \u1045 \u1053 \u1044 \u1040 \u1062 \u1048 \u1071 .\\n",\
\
        'help_message_close_button': "\uc0\u1047 \u1072 \u1082 \u1088 \u1099 \u1090 \u1100 ",\
        'top10_rise_button': "\uc0\u1058 \u1086 \u1087  10 \u1088 \u1086 \u1089 \u1090  \u55357 \u56960 ",\
        'top10_fall_button': "\uc0\u1058 \u1086 \u1087  10 \u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103  \u55357 \u56521 ",\
        'help_button': "\uc0\u10067  \u1055 \u1086 \u1084 \u1086 \u1097 \u1100 ",\
        'donat_button': "\uc0\u55357 \u56496  Donat",\
        'back_button': "\uc0\u1053 \u1072 \u1079 \u1072 \u1076 ",\
        'english_button': "English",\
        'russian_button': "\uc0\u1056 \u1091 \u1089 \u1089 \u1082 \u1080 \u1081 ",\
        'top10_rise_header': "\uc0\u55357 \u56960  **\u1058 \u1086 \u1087  10 \u1084 \u1086 \u1085 \u1077 \u1090  \u1088 \u1086 \u1089 \u1090  (Binance):**\\n\\n",\
        'top10_fall_header': "\uc0\u55357 \u56521  **\u1058 \u1086 \u1087  10 \u1084 \u1086 \u1085 \u1077 \u1090  \u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103  (Binance):**\\n\\n",\
        'binance_data_unavailable_fallback_rise': "\uc0\u9888 \u65039  Binance data unavailable, using CoinGecko trending as fallback for top 10 rising coins:\\n\\n",\
        'binance_data_unavailable_fallback_fall': "\uc0\u9888 \u65039  Binance data unavailable, using CoinGecko trending as fallback for top 10 falling coins:\\n\\n",\
        'error_fetching_top10_rise': "\uc0\u9888 \u65039  Error fetching top 10 rising coins.",\
        'error_fetching_top10_fall': "\uc0\u9888 \u65039  Error fetching top 10 falling coins.",\
        'price_in_usdt': "\{:.5f\} $",\
        'price_in_crypto': "\{:.5f\} \{\}",\
        'error_fetching_price_usdt': "\uc0\u9888 \u65039  Error fetching price for \{\} in USDT",\
        'error_fetching_price_crypto': "\uc0\u9888 \u65039  Error fetching price for \{\} in \{\}",\
        'invalid_input_amount_coin_coin': "\uc0\u9888 \u65039  Invalid input. Please use format: amount COIN1 COIN2 (e.g., 12 SUI USDT or 10 STRK TWT)",\
        'invalid_input_amount_coin_coin_index_error': "\uc0\u9888 \u65039  Invalid input. Please use format: amount COIN1 COIN2 (e.g., 12 SUI USDT or 10 STRK TWT)",\
        'error_fetching_data': "\uc0\u9888 \u65039  \u1054 \u1096 \u1080 \u1073 \u1082 \u1072  \u1087 \u1086 \u1083 \u1091 \u1095 \u1077 \u1085 \u1080 \u1103  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093 ",\
        'error_invalid_ticker': " ",  # \uc0\u1053 \u1054 \u1042 \u1054 \u1045  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077  \u1086 \u1073  \u1086 \u1096 \u1080 \u1073 \u1082 \u1077 \
        'price_coin': "\uc0\u55357 \u56496  **\{\} Price:** $\{:.5f\}\\n",\
        'change_24h': "\uc0\u55357 \u56520  24h Change: \{:.5f\}%\\n",\
        'signal_24h': "\uc0\u55357 \u56596  **Signal (24h):** \{\}\\n",\
        'trend_24h': "\uc0\u55357 \u56522  **Trend (24h):** \{\}",\
        'button_1h': "1h",\
        'button_4h': "4h",\
        'button_12h': "12h",\
        'not_enough_historical_data': "\uc0\u9888 \u65039  Not enough historical data for this timeframe.",\
        'timeframe_change': "\uc0\u55357 \u56520  \{\} Change: \{:.5f\}%\\n",\
        'signal_timeframe': "\uc0\u55357 \u56596  **Signal (\{\}):** \{\}\\n",\
        'trend_timeframe': "\uc0\u55357 \u56522  **Trend (\{\}):** \{\}",\
        'error_fetching_timeframe_data': "\uc0\u9888 \u65039  Error fetching data for timeframe.",\
        'donat_message': "\uc0\u55357 \u56911  \u1055 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1080 \u1090 \u1077  \u1088 \u1072 \u1079 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082 \u1072 , \u1095 \u1090 \u1086 \u1073 \u1099  \u1073 \u1086 \u1090  \u1087 \u1088 \u1086 \u1076 \u1086 \u1083 \u1078 \u1072 \u1083  \u1088 \u1072 \u1076 \u1086 \u1074 \u1072 \u1090 \u1100  \u1074 \u1072 \u1089  \u1085 \u1086 \u1074 \u1099 \u1084 \u1080  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103 \u1084 \u1080  \u1080  \u1091 \u1083 \u1091 \u1095 \u1096 \u1077 \u1085 \u1080 \u1103 \u1084 \u1080 !\\n\\n"\
                         "\uc0\u8383  **BTC:** `bc1qcategq6gf69ytjz9a8ldavy2yjuc6f67zexsns`\\n"\
                         "\\n"\
                         "\uc0\u55357 \u56498  **USDT (TRC20):** `TYndQoBjYDMn2r4GZ5JqYyS5oJvJ1tYLi7`\\n\\n"\
                         "\uc0\u1057 \u1087 \u1072 \u1089 \u1080 \u1073 \u1086  \u1079 \u1072  \u1074 \u1072 \u1096 \u1091  \u1087 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1082 \u1091 !",\
        'language_switch_developing': "\uc0\u1060 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103  \u1087 \u1077 \u1088 \u1077 \u1082 \u1083 \u1102 \u1095 \u1077 \u1085 \u1080 \u1103  \u1085 \u1072  \u1072 \u1085 \u1075 \u1083 \u1080 \u1081 \u1089 \u1082 \u1080 \u1081  \u1074  \u1088 \u1072 \u1079 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1077 !",\
        'trend_ascending': "\uc0\u55357 \u57314  \u1042 \u1086 \u1089 \u1093 \u1086 \u1076 \u1103 \u1097 \u1080 \u1081 ",\
        'trend_descending': "\uc0\u55357 \u56628  \u1053 \u1080 \u1089 \u1093 \u1086 \u1076 \u1103 \u1097 \u1080 \u1081 ",\
        'trend_sideways': "\uc0\u10134  \u1041 \u1086 \u1082 \u1086 \u1074 \u1086 \u1081 ",\
        'trend_strength_strong': " (\uc0\u1057 \u1080 \u1083 \u1100 \u1085 \u1099 \u1081 )",\
        'trend_strength_weak': " (\uc0\u1057 \u1083 \u1072 \u1073 \u1099 \u1081 )",\
        'signal_buy': "BUY \uc0\u55357 \u56520 ",\
        'signal_sell': "SELL \uc0\u55357 \u56521 ",\
        'signal_hold': "HOLD \uc0\u9878 ",\
        'interval_1h': '1h',\
        'interval_4h': '4h',\
        'interval_8h': '8h',\
        'interval_12h': '12h',\
        'interval_24h': '24h',\
        'interval_1d': '24h',\
        'interval_change': 'Change',\
    \},\
    'en': \{\
        'start_message': "\uc0\u55357 \u56522  Choose an action or enter a ticker or request (e.g., BTC, 12 SUI USDT, 10 STRK TWT):",\
        'help_message_header': "\uc0\u55357 \u56481  **How to use the bot:**\\n\\n",\
        'help_message_calculation_header': "**For price calculation:**\\n",\
        'help_message_calculation_text': "Enter the amount and coin pair, for example: `12 SUI USDT` or `0.5 ETH BTC` or `10 STRK TWT`.\\n"\
        "- The bot will return the value of the specified amount of the first coin in the second currency.\\n"\
        "- For USDT pairs, the price will be shown in dollars ($).\\n"\
        "- For crypto-crypto pairs (e.g., ETH BTC, STRK TWT), the price will be shown in the second cryptocurrency.\\n\\n",\
        'help_message_calculation_examples_header': "**Examples of calculation requests:**\\n",\
        'help_message_calculation_examples_text': "- `12 SUI USDT` - find out the cost of 12 SUI in US dollars.\\n"\
        "- `0.5 ETH BTC` - find out the cost of 0.5 ETH in BTC.\\n"\
        "- `10 STRK TWT` - find out the cost of 10 STRK TWT.\\n\\n",\
        'help_message_technical_analysis_header': "**To get technical analysis (calculator) with different timeframes:**\\n",\
        'help_message_technical_analysis_text': "Just enter the coin ticker (e.g., `BTC`, `ETH`, `SUI`). The bot will show:\\n"\
                                                  "- Current price (always)\\n"\
                                                  "- Price change for the selected timeframe in percent\\n"\
                                                  "- Trading signal and trend for the selected timeframe\\n"\
                                                  "- Buttons to switch to technical analysis for timeframes: 1h, 4h, 12h, Back\\n"\
                                                  "**You can switch the bot language to English or Russian by pressing the corresponding buttons below.**\\n\\n",\
        'help_message_technical_analysis_features_header': "**Supported technical analysis functions:**\\n",\
        'help_message_technical_analysis_features_text': "- RSI (Relative Strength Index)\\n"\
        "- MACD (Moving Average Convergence/Divergence)\\n"\
        # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  30 \u1080  100\
        "- EMA (Exponential Moving Average) - 30 and 100 periods\\n"\
        "- Bollinger Bands\\n"\
        "- Stochastic Oscillator\\n"\
        "- SMA (Simple Moving Average) - 20 and 50 periods\\n"\
        "- Parabolic SAR (Parabolic SAR system)\\n"\
        "- ADX (Average Directional Index)\\n"\
        "- Ichimoku Cloud\\n"\
        "- Williams %R (Williams Percent Range)\\n"\
        "- **OBV (On Balance Volume)**\\n"\
        "- Support and resistance levels\\n"\
        "- Fibonacci Levels\\n",\
        'help_message_other_functions_header': "**Other functions:**\\n",\
        'help_message_other_functions_text': "- The 'Top 10 Rise \uc0\u55357 \u56960 ' and 'Top 10 Fall \u55357 \u56521 ' sections show the top gainers and losers on Binance.\\n"\
                                               "- The 'Help' section - current help.\\n"\
                                               "- The 'Donat' section - to support the developer.\\n"\
                                               "- NOT A FINANCIAL RECOMMENDATION.\\n",\
        'help_message_close_button': "Close",\
        'top10_rise_button': "Top 10 Rise \uc0\u55357 \u56960 ",\
        'top10_fall_button': "Top 10 Fall \uc0\u55357 \u56521 ",\
        'help_button': "\uc0\u10067  Help",\
        'donat_button': "\uc0\u55357 \u56496  Donate",\
        'back_button': "Back",\
        'english_button': "English",\
        'russian_button': "Russian",\
        'top10_rise_header': "\uc0\u55357 \u56960  **Top 10 Rising Coins (Binance):**\\n\\n",\
        'top10_fall_header': "\uc0\u55357 \u56521  **Top 10 Falling Coins (Binance):**\\n\\n",\
        'binance_data_unavailable_fallback_rise': "\uc0\u9888 \u65039  Binance data unavailable, using CoinGecko trending as fallback for top 10 rising coins:\\n\\n",\
        'binance_data_unavailable_fallback_fall': "\uc0\u9888 \u65039  Binance data unavailable, using CoinGecko trending as fallback for top 10 falling coins:\\n\\n",\
        'error_fetching_top10_rise': "\uc0\u9888 \u65039  Error fetching top 10 rising coins.",\
        'error_fetching_top10_fall': "\uc0\u9888 \u65039  Error fetching top 10 falling coins.",\
        'price_in_usdt': "\{:.5f\} $",\
        'price_in_crypto': "\{:.5f\} \{\}",\
        'error_fetching_price_usdt': "\uc0\u9888 \u65039  Error fetching price for \{\} in USDT",\
        'error_fetching_price_crypto': "\uc0\u9888 \u65039  Error fetching price for \{\} in \{\}",\
        'invalid_input_amount_coin_coin': "\uc0\u9888 \u65039  Invalid input. Please use format: amount COIN1 COIN2 (e.g., 12 SUI USDT or 10 STRK TWT)",\
        'invalid_input_amount_coin_coin_index_error': "\uc0\u9888 \u65039  Invalid input. Please use format: amount COIN1 COIN2 (e.g., 12 SUI USDT or 10 STRK TWT)",\
        'error_fetching_data': "\uc0\u9888 \u65039  Error fetching data",\
        'error_invalid_ticker': "\{\}  ",  # NEW error message\
        'price_coin': "\uc0\u55357 \u56496  **\{\} Price:** $\{:.5f\}\\n",\
        'change_24h': "\uc0\u55357 \u56520  24h Change: \{:.5f\}%\\n",\
        'signal_24h': "\uc0\u55357 \u56596  **Signal (24h):** \{\}\\n",\
        'trend_24h': "\uc0\u55357 \u56522  **Trend (24h):** \{\}",\
        'button_1h': "1h",\
        'button_4h': "4h",\
        'button_12h': "12h",\
        'not_enough_historical_data': "\uc0\u9888 \u65039  Not enough historical data for this timeframe.",\
        'timeframe_change': "\uc0\u55357 \u56520  \{\} Change: \{:.5f\}%\\n",\
        'signal_timeframe': "\uc0\u55357 \u56596  **Signal (\{\}):** \{\}\\n",\
        'trend_timeframe': "\uc0\u55357 \u56522  **Trend (\{\}):** \{\}",\
        'error_fetching_timeframe_data': "\uc0\u9888 \u65039  Error fetching data for timeframe.",\
        'donat_message': "\uc0\u55357 \u56911  Support the developer so that the bot continues to delight you with new features and improvements!\\n\\n"\
                         "\uc0\u8383  **BTC:** `bc1qcategq6gf69ytjz9a8ldavy2yjuc6f67zexsns`\\n"\
                         "\\n"\
                         "\uc0\u55357 \u56498  **USDT (TRC20):** `TYndQoBjYDMn2r4GZ5JqYyS5oJvJ1tYLi7`\\n\\n"\
                         "Thank you for your support!",\
        'language_switch_developing': "Language switch to English is under development!",\
        'trend_ascending': "\uc0\u55357 \u57314  Ascending",\
        'trend_descending': "\uc0\u55357 \u56628  Descending",\
        'trend_sideways': "\uc0\u10134  Sideways",\
        'trend_strength_strong': " (Strong)",\
        'trend_strength_weak': " (Weak)",\
        'signal_buy': "BUY \uc0\u55357 \u56520 ",\
        'signal_sell': "SELL \uc0\u55357 \u56521 ",\
        'signal_hold': "HOLD \uc0\u9878 ",\
        'interval_1h': '1h',\
        'interval_4h': '4h',\
        'interval_8h': '8h',\
        'interval_12h': '12h',\
        'interval_24h': '24h',\
        'interval_1d': '24h',\
        'interval_change': 'Change',\
    \},\
\}\
\
# --- \uc0\u1043 \u1083 \u1086 \u1073 \u1072 \u1083 \u1100 \u1085 \u1072 \u1103  \u1087 \u1077 \u1088 \u1077 \u1084 \u1077 \u1085 \u1085 \u1072 \u1103  \u1076 \u1083 \u1103  \u1103 \u1079 \u1099 \u1082 \u1072  (\u1059 \u1044 \u1040 \u1051 \u1045 \u1053 \u1040 ) ---\
# BOT_LANGUAGE = 'ru'  # \uc0\u1055 \u1086  \u1091 \u1084 \u1086 \u1083 \u1095 \u1072 \u1085 \u1080 \u1102  \u1088 \u1091 \u1089 \u1089 \u1082 \u1080 \u1081  \u1103 \u1079 \u1099 \u1082  (\u1059 \u1044 \u1040 \u1051 \u1045 \u1053 \u1054  - \u1090 \u1077 \u1087 \u1077 \u1088 \u1100  \u1103 \u1079 \u1099 \u1082  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  \u1093 \u1088 \u1072 \u1085 \u1080 \u1090 \u1089 \u1103  \u1074  \u1041 \u1044 )\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  1.1: \u1056 \u1072 \u1073 \u1086 \u1090 \u1072  \u1089  \u1073 \u1072 \u1079 \u1086 \u1081  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093  SQLite\
# ======================================================================\
\
DATABASE_NAME = 'crypto_bot.db'  # \uc0\u1048 \u1084 \u1103  \u1092 \u1072 \u1081 \u1083 \u1072  \u1073 \u1072 \u1079 \u1099  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093 \
\
\
def create_connection():\
    """\uc0\u1057 \u1086 \u1079 \u1076 \u1072 \u1077 \u1090  \u1087 \u1086 \u1076 \u1082 \u1083 \u1102 \u1095 \u1077 \u1085 \u1080 \u1077  \u1082  \u1073 \u1072 \u1079 \u1077  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093  SQLite."""\
    conn = None\
    try:\
        conn = sqlite3.connect(DATABASE_NAME)\
        return conn\
    except sqlite3.Error as e:\
        print(f"Database connection error: \{e\}")\
    return conn\
\
\
def create_tables():\
    """\uc0\u1057 \u1086 \u1079 \u1076 \u1072 \u1077 \u1090  \u1090 \u1072 \u1073 \u1083 \u1080 \u1094 \u1099  \u1074  \u1073 \u1072 \u1079 \u1077  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093 , \u1077 \u1089 \u1083 \u1080  \u1086 \u1085 \u1080  \u1085 \u1077  \u1089 \u1091 \u1097 \u1077 \u1089 \u1090 \u1074 \u1091 \u1102 \u1090 ."""\
    conn = create_connection()\
    if conn is not None:\
        try:\
            cursor = conn.cursor()\
            # \uc0\u1058 \u1072 \u1073 \u1083 \u1080 \u1094 \u1072  \u1076 \u1083 \u1103  \u1093 \u1088 \u1072 \u1085 \u1077 \u1085 \u1080 \u1103  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1077 \u1082  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  (\u1087 \u1088 \u1080 \u1084 \u1077 \u1088 )\
            cursor.execute("""\
                CREATE TABLE IF NOT EXISTS user_settings (\
                    user_id INTEGER PRIMARY KEY,\
                    language TEXT DEFAULT 'ru',\
                    preferred_timeframe TEXT DEFAULT '24h'\
                    -- \uc0\u1047 \u1076 \u1077 \u1089 \u1100  \u1084 \u1086 \u1078 \u1085 \u1086  \u1076 \u1086 \u1073 \u1072 \u1074 \u1080 \u1090 \u1100  \u1076 \u1088 \u1091 \u1075 \u1080 \u1077  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1080  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103 \
                )\
            """)\
            conn.commit()\
        except sqlite3.Error as e:\
            print(f"Database table creation error: \{e\}")\
        finally:\
            conn.close()\
    else:\
        print("Error: Cannot create database connection.")\
\
\
def get_user_setting(user_id, setting_name):\
    """\uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1090  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1091  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  \u1080 \u1079  \u1073 \u1072 \u1079 \u1099  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093 ."""\
    conn = create_connection()\
    setting_value = None\
    if conn is not None:\
        try:\
            cursor = conn.cursor()\
            cursor.execute(\
                f"SELECT \{setting_name\} FROM user_settings WHERE user_id=?", (user_id,))\
            row = cursor.fetchone()\
            if row:\
                setting_value = row[0]\
        except sqlite3.Error as e:\
            print(f"Database get setting error: \{e\}")\
        finally:\
            conn.close()\
    return setting_value\
\
\
def set_user_setting(user_id, setting_name, setting_value):\
    """\uc0\u1059 \u1089 \u1090 \u1072 \u1085 \u1072 \u1074 \u1083 \u1080 \u1074 \u1072 \u1077 \u1090  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1091  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  \u1074  \u1073 \u1072 \u1079 \u1077  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093 ."""\
    conn = create_connection()\
    if conn is not None:\
        try:\
            cursor = conn.cursor()\
            # \uc0\u1057 \u1085 \u1072 \u1095 \u1072 \u1083 \u1072  \u1087 \u1088 \u1086 \u1074 \u1077 \u1088 \u1103 \u1077 \u1084 , \u1077 \u1089 \u1090 \u1100  \u1083 \u1080  \u1091 \u1078 \u1077  \u1079 \u1072 \u1087 \u1080 \u1089 \u1100  \u1076 \u1083 \u1103  user_id\
            cursor.execute(\
                "SELECT user_id FROM user_settings WHERE user_id=?", (user_id,))\
            existing_user = cursor.fetchone()\
            if existing_user:\
                # \uc0\u1045 \u1089 \u1083 \u1080  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1100  \u1091 \u1078 \u1077  \u1077 \u1089 \u1090 \u1100 , \u1086 \u1073 \u1085 \u1086 \u1074 \u1083 \u1103 \u1077 \u1084  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1091 \
                cursor.execute(\
                    f"UPDATE user_settings SET \{setting_name\}=? WHERE user_id=?", (setting_value, user_id))\
            else:\
                # \uc0\u1045 \u1089 \u1083 \u1080  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  \u1085 \u1077 \u1090 , \u1089 \u1086 \u1079 \u1076 \u1072 \u1077 \u1084  \u1085 \u1086 \u1074 \u1091 \u1102  \u1079 \u1072 \u1087 \u1080 \u1089 \u1100  \u1089  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1081 \u1082 \u1086 \u1081 \
                cursor.execute(\
                    f"INSERT INTO user_settings (user_id, \{setting_name\}) VALUES (?, ?)", (user_id, setting_value))\
            conn.commit()\
        except sqlite3.Error as e:\
            print(f"Database set setting error: \{e\}")\
        finally:\
            conn.close()\
\
# \uc0\u1060 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103  \u1076 \u1083 \u1103  \u1087 \u1086 \u1083 \u1091 \u1095 \u1077 \u1085 \u1080 \u1103  \u1103 \u1079 \u1099 \u1082 \u1072  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  (\u1087 \u1088 \u1080 \u1084 \u1077 \u1088  \u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1085 \u1080 \u1103  get_user_setting)\
\
\
def get_user_language(user_id):\
    """\uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1090  \u1103 \u1079 \u1099 \u1082  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  \u1080 \u1079  \u1073 \u1072 \u1079 \u1099  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093 , \u1087 \u1086  \u1091 \u1084 \u1086 \u1083 \u1095 \u1072 \u1085 \u1080 \u1102  'ru'."""\
    language = get_user_setting(user_id, 'language')\
    return language if language else 'ru'  # \uc0\u1055 \u1086  \u1091 \u1084 \u1086 \u1083 \u1095 \u1072 \u1085 \u1080 \u1102  \u1088 \u1091 \u1089 \u1089 \u1082 \u1080 \u1081 \
\
# \uc0\u1060 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103  \u1076 \u1083 \u1103  \u1091 \u1089 \u1090 \u1072 \u1085 \u1086 \u1074 \u1082 \u1080  \u1103 \u1079 \u1099 \u1082 \u1072  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  (\u1087 \u1088 \u1080 \u1084 \u1077 \u1088  \u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1085 \u1080 \u1103  set_user_setting)\
\
\
def set_user_language(user_id, language):\
    """\uc0\u1059 \u1089 \u1090 \u1072 \u1085 \u1072 \u1074 \u1083 \u1080 \u1074 \u1072 \u1077 \u1090  \u1103 \u1079 \u1099 \u1082  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  \u1074  \u1073 \u1072 \u1079 \u1077  \u1076 \u1072 \u1085 \u1085 \u1099 \u1093 ."""\
    set_user_setting(user_id, 'language', language)\
\
\
# \uc0\u1055 \u1088 \u1080  \u1079 \u1072 \u1087 \u1091 \u1089 \u1082 \u1077  \u1073 \u1086 \u1090 \u1072  \u1089 \u1086 \u1079 \u1076 \u1072 \u1077 \u1084  \u1090 \u1072 \u1073 \u1083 \u1080 \u1094 \u1099 , \u1077 \u1089 \u1083 \u1080  \u1080 \u1093  \u1085 \u1077 \u1090 \
create_tables()\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  2: \u1060 \u1091 \u1085 \u1082 \u1094 \u1080 \u1080  \u1076 \u1083 \u1103  \u1088 \u1072 \u1073 \u1086 \u1090 \u1099  \u1089  Binance API\
# ======================================================================\
\
def get_binance_price(coin_id: str):\
    """\
    \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1090  24-\u1095 \u1072 \u1089 \u1086 \u1074 \u1091 \u1102  \u1089 \u1074 \u1086 \u1076 \u1082 \u1091  \u1087 \u1086  \u1090 \u1080 \u1082 \u1077 \u1088 \u1091  \u1089  Binance API.\
\
    Args:\
        coin_id (str): \uc0\u1057 \u1080 \u1084 \u1074 \u1086 \u1083  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 , BTC).\
\
    Returns:\
        dict: \uc0\u1044 \u1072 \u1085 \u1085 \u1099 \u1077  \u1090 \u1080 \u1082 \u1077 \u1088 \u1072  \u1074  \u1092 \u1086 \u1088 \u1084 \u1072 \u1090 \u1077  JSON \u1080 \u1083 \u1080  None \u1074  \u1089 \u1083 \u1091 \u1095 \u1072 \u1077  \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 .\
    """\
    try:\
        url = "https://api.binance.com/api/v3/ticker/24hr"\
        params = \{'symbol': f"\{coin_id.upper()\}USDT"\}\
        response = requests.get(url, params=params)\
        response.raise_for_status()  # \uc0\u1055 \u1088 \u1086 \u1074 \u1077 \u1088 \u1082 \u1072  \u1085 \u1072  HTTP \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 \
        ticker = response.json()\
        return ticker\
    except requests.exceptions.RequestException as e:\
        logger.error(\
            f"Binance API error (get_binance_price for \{coin_id\}): \{e\}")\
        return None\
\
\
def get_binance_price_direct(coin1_id: str, coin2_id: str):\
    """\
    \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1090  \u1094 \u1077 \u1085 \u1091  \u1087 \u1088 \u1103 \u1084 \u1086 \u1081  \u1090 \u1086 \u1088 \u1075 \u1086 \u1074 \u1086 \u1081  \u1087 \u1072 \u1088 \u1099  \u1089  Binance API.\
\
    Args:\
        coin1_id (str): \uc0\u1057 \u1080 \u1084 \u1074 \u1086 \u1083  \u1087 \u1077 \u1088 \u1074 \u1086 \u1081  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 , ETH).\
        coin2_id (str): \uc0\u1057 \u1080 \u1084 \u1074 \u1086 \u1083  \u1074 \u1090 \u1086 \u1088 \u1086 \u1081  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 , BTC).\
\
    Returns:\
        float: \uc0\u1062 \u1077 \u1085 \u1072  \u1090 \u1086 \u1088 \u1075 \u1086 \u1074 \u1086 \u1081  \u1087 \u1072 \u1088 \u1099  \u1080 \u1083 \u1080  None \u1074  \u1089 \u1083 \u1091 \u1095 \u1072 \u1077  \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 .\
    """\
    try:\
        symbol = f"\{coin1_id.upper()\}\{coin2_id.upper()\}"\
        url = "https://api.binance.com/api/v3/ticker/price"\
        params = \{'symbol': symbol\}\
        response = requests.get(url, params=params)\
        response.raise_for_status()  # \uc0\u1055 \u1088 \u1086 \u1074 \u1077 \u1088 \u1082 \u1072  \u1085 \u1072  HTTP \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 \
        price_data = response.json()\
        return float(price_data['price'])\
    except requests.exceptions.RequestException as e:\
        logger.error(\
            f"Binance API error (get_binance_price_direct for \{coin1_id\}-\{coin2_id\}): \{e\}")\
        return None\
\
\
def get_binance_top_movers(limit=10, sort_by='priceChangePercent', ascending=False):\
    """\
    \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1090  \u1089 \u1087 \u1080 \u1089 \u1086 \u1082  \u1083 \u1080 \u1076 \u1077 \u1088 \u1086 \u1074  \u1088 \u1086 \u1089 \u1090 \u1072 /\u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103  \u1089  Binance API.\
\
    Args:\
        limit (int): \uc0\u1052 \u1072 \u1082 \u1089 \u1080 \u1084 \u1072 \u1083 \u1100 \u1085 \u1086 \u1077  \u1082 \u1086 \u1083 \u1080 \u1095 \u1077 \u1089 \u1090 \u1074 \u1086  \u1084 \u1086 \u1085 \u1077 \u1090  \u1074  \u1089 \u1087 \u1080 \u1089 \u1082 \u1077 .\
        sort_by (str): \uc0\u1055 \u1072 \u1088 \u1072 \u1084 \u1077 \u1090 \u1088  \u1076 \u1083 \u1103  \u1089 \u1086 \u1088 \u1090 \u1080 \u1088 \u1086 \u1074 \u1082 \u1080  ('priceChangePercent', 'volume' \u1080  \u1076 \u1088 .).\
        ascending (bool): \uc0\u1057 \u1086 \u1088 \u1090 \u1080 \u1088 \u1086 \u1074 \u1072 \u1090 \u1100  \u1087 \u1086  \u1074 \u1086 \u1079 \u1088 \u1072 \u1089 \u1090 \u1072 \u1085 \u1080 \u1102  (True \u1076 \u1083 \u1103  \u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103 , False \u1076 \u1083 \u1103  \u1088 \u1086 \u1089 \u1090 \u1072 ).\
\
    Returns:\
        list: \uc0\u1057 \u1087 \u1080 \u1089 \u1086 \u1082  \u1082 \u1086 \u1088 \u1090 \u1077 \u1078 \u1077 \u1081  \u1089  \u1076 \u1072 \u1085 \u1085 \u1099 \u1084 \u1080  \u1086  \u1083 \u1080 \u1076 \u1077 \u1088 \u1072 \u1093  \u1088 \u1086 \u1089 \u1090 \u1072 /\u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103  \u1080 \u1083 \u1080  None \u1074  \u1089 \u1083 \u1091 \u1095 \u1072 \u1077  \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 .\
              \uc0\u1050 \u1072 \u1078 \u1076 \u1099 \u1081  \u1082 \u1086 \u1088 \u1090 \u1077 \u1078  \u1089 \u1086 \u1076 \u1077 \u1088 \u1078 \u1080 \u1090  (\u1089 \u1080 \u1084 \u1074 \u1086 \u1083 , \u1080 \u1084 \u1103 , \u1090 \u1077 \u1082 \u1091 \u1097 \u1072 \u1103  \u1094 \u1077 \u1085 \u1072 , \u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1080 \u1077  \u1094 \u1077 \u1085 \u1099  \u1079 \u1072  24\u1095  \u1074  \u1087 \u1088 \u1086 \u1094 \u1077 \u1085 \u1090 \u1072 \u1093 ).\
    """\
    try:\
        url = "https://api.binance.com/api/v3/ticker/24hr"\
        response = requests.get(url)\
        response.raise_for_status()  # \uc0\u1055 \u1088 \u1086 \u1074 \u1077 \u1088 \u1082 \u1072  \u1085 \u1072  HTTP \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 \
        tickers = response.json()\
\
        # Filter USDT pairs and remove pairs without USDT\
        usdt_tickers = [\
            ticker for ticker in tickers if ticker['symbol'].endswith('USDT') and ticker['symbol'] != 'USDTUSDT'\
        ]\
\
        # Sort tickers\
        sorted_tickers = sorted(\
            usdt_tickers,\
            key=lambda x: float(x[sort_by]),\
            # ascending=False for \uc0\u1088 \u1086 \u1089 \u1090  (\u1087 \u1086  \u1091 \u1073 \u1099 \u1074 \u1072 \u1085 \u1080 \u1102 ), ascending=True \u1076 \u1083 \u1103  \u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103  (\u1087 \u1086  \u1074 \u1086 \u1079 \u1088 \u1072 \u1089 \u1090 \u1072 \u1085 \u1080 \u1102 )\
            reverse=not ascending\
        )\
\
        top_movers = []\
        for ticker in sorted_tickers[:limit]:\
            symbol = ticker['symbol'].replace('USDT', '')\
            top_movers.append((\
                symbol,\
                symbol,  # \uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1084  \u1089 \u1080 \u1084 \u1074 \u1086 \u1083  \u1082 \u1072 \u1082  \u1080 \u1084 \u1103  \u1076 \u1083 \u1103  \u1089 \u1086 \u1074 \u1084 \u1077 \u1089 \u1090 \u1080 \u1084 \u1086 \u1089 \u1090 \u1080 \
                float(ticker['lastPrice']),\
                float(ticker['priceChangePercent'])\
            ))\
        return top_movers\
\
    except requests.exceptions.RequestException as e:\
        logger.error(f"Binance API error (get_binance_top_movers): \{e\}")\
        return None\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  3: \u1060 \u1091 \u1085 \u1082 \u1094 \u1080 \u1080  \u1076 \u1083 \u1103  \u1088 \u1072 \u1073 \u1086 \u1090 \u1099  \u1089  CoinGecko API\
#                       (\uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1102 \u1090 \u1089 \u1103  \u1082 \u1072 \u1082  \u1079 \u1072 \u1087 \u1072 \u1089 \u1085 \u1086 \u1081  \u1074 \u1072 \u1088 \u1080 \u1072 \u1085 \u1090  \u1080  \u1076 \u1083 \u1103  \u1090 \u1086 \u1095 \u1085 \u1099 \u1093  \u1094 \u1077 \u1085 )\
# ======================================================================\
\
def get_coingecko_price(coin_id: str, vs_currency='usd'):\
    """\
    \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1090  \u1090 \u1077 \u1082 \u1091 \u1097 \u1091 \u1102  \u1094 \u1077 \u1085 \u1091  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  \u1089  CoinGecko API.\
\
    Args:\
        coin_id (str): ID \uc0\u1084 \u1086 \u1085 \u1077 \u1090 \u1099  \u1085 \u1072  CoinGecko (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 , bitcoin, ethereum).  \u1042 \u1072 \u1078 \u1085 \u1086  \u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1100  ID CoinGecko, \u1072  \u1085 \u1077  \u1089 \u1080 \u1084 \u1074 \u1086 \u1083 .\
        vs_currency (str): \uc0\u1042 \u1072 \u1083 \u1102 \u1090 \u1072 , \u1074  \u1082 \u1086 \u1090 \u1086 \u1088 \u1086 \u1081  \u1085 \u1091 \u1078 \u1085 \u1086  \u1087 \u1086 \u1083 \u1091 \u1095 \u1080 \u1090 \u1100  \u1094 \u1077 \u1085 \u1091  (\u1087 \u1086  \u1091 \u1084 \u1086 \u1083 \u1095 \u1072 \u1085 \u1080 \u1102  'usd').\
\
    Returns:\
        float: \uc0\u1062 \u1077 \u1085 \u1072  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  \u1074  \u1091 \u1082 \u1072 \u1079 \u1072 \u1085 \u1085 \u1086 \u1081  \u1074 \u1072 \u1083 \u1102 \u1090 \u1077  \u1080 \u1083 \u1080  None \u1074  \u1089 \u1083 \u1091 \u1095 \u1072 \u1077  \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 .\
    """\
    try:\
        url = f"https://api.coingecko.com/api/v3/simple/price?ids=\{coin_id\}&vs_currencies=\{vs_currency\}"\
        response = requests.get(url)\
        response.raise_for_status()\
        data = response.json()\
        if coin_id in data and vs_currency in data[coin_id]:\
            return float(data[coin_id][vs_currency])\
        else:\
            logger.warning(\
                f"CoinGecko API: Price not found for \{coin_id\} in \{vs_currency\}")\
            return None\
    except requests.exceptions.RequestException as e:\
        logger.error(\
            f"CoinGecko API error (get_coingecko_price for \{coin_id\}): \{e\}")\
        return None\
\
\
def get_coingecko_coin_id_by_symbol(symbol: str):\
    """\
    \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1090  CoinGecko Coin ID \u1087 \u1086  \u1089 \u1080 \u1084 \u1074 \u1086 \u1083 \u1091  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099 .\
\
    Args:\
        symbol (str): \uc0\u1057 \u1080 \u1084 \u1074 \u1086 \u1083  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 , BTC).\
\
    Returns:\
        str: CoinGecko Coin ID \uc0\u1080 \u1083 \u1080  None, \u1077 \u1089 \u1083 \u1080  \u1085 \u1077  \u1085 \u1072 \u1081 \u1076 \u1077 \u1085 .\
    """\
    try:\
        url = f"https://api.coingecko.com/api/v3/coins/list?include_platform=false"\
        response = requests.get(url)\
        response.raise_for_status()\
        coins_list = response.json()\
        for coin in coins_list:\
            if coin['symbol'].upper() == symbol.upper():  # \uc0\u1057 \u1088 \u1072 \u1074 \u1085 \u1080 \u1074 \u1072 \u1077 \u1084  \u1089 \u1080 \u1084 \u1074 \u1086 \u1083 \u1099  \u1074  \u1074 \u1077 \u1088 \u1093 \u1085 \u1077 \u1084  \u1088 \u1077 \u1075 \u1080 \u1089 \u1090 \u1088 \u1077 \
                return coin['id']\
        logger.warning(f"CoinGecko API: Coin ID not found for symbol \{symbol\}")\
        return None\
    except requests.exceptions.RequestException as e:\
        logger.error(\
            f"CoinGecko API error (get_coingecko_coin_id_by_symbol for \{symbol\}): \{e\}")\
        return None\
\
\
def get_trending_coins():\
    """\
    \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1090  \u1089 \u1087 \u1080 \u1089 \u1086 \u1082  \u1090 \u1088 \u1077 \u1085 \u1076 \u1086 \u1074 \u1099 \u1093  \u1084 \u1086 \u1085 \u1077 \u1090  \u1089  CoinGecko API.\
\
    Returns:\
        list: \uc0\u1057 \u1087 \u1080 \u1089 \u1086 \u1082  \u1082 \u1086 \u1088 \u1090 \u1077 \u1078 \u1077 \u1081  \u1089  \u1076 \u1072 \u1085 \u1085 \u1099 \u1084 \u1080  \u1086  \u1090 \u1088 \u1077 \u1085 \u1076 \u1086 \u1074 \u1099 \u1093  \u1084 \u1086 \u1085 \u1077 \u1090 \u1072 \u1093  \u1080 \u1083 \u1080  None \u1074  \u1089 \u1083 \u1091 \u1095 \u1072 \u1077  \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 .\
              \uc0\u1050 \u1072 \u1078 \u1076 \u1099 \u1081  \u1082 \u1086 \u1088 \u1090 \u1077 \u1078  \u1089 \u1086 \u1076 \u1077 \u1088 \u1078 \u1080 \u1090  (\u1089 \u1080 \u1084 \u1074 \u1086 \u1083 , \u1080 \u1084 \u1103 , \u1094 \u1077 \u1085 \u1072 , \u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1080 \u1077  \u1094 \u1077 \u1085 \u1099  \u1079 \u1072  24\u1095  \u1074  \u1087 \u1088 \u1086 \u1094 \u1077 \u1085 \u1090 \u1072 \u1093 ).\
    """\
    try:\
        url = "https://api.coingecko.com/api/v3/search/trending"\
        response = requests.get(url)\
        response.raise_for_status()  # \uc0\u1055 \u1088 \u1086 \u1074 \u1077 \u1088 \u1082 \u1072  \u1085 \u1072  HTTP \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 \
        data = response.json()\
        return [\
            (coin["item"]["symbol"].upper(),\
             coin["item"]["name"],\
             # Convert to float and remove commas\
             float(coin["item"]["data"]["price"].replace(',', '')),\
             float(coin["item"]["data"]["price_change_percentage_24h"]["usd"]))\
            for coin in data["coins"][:10]  # Get top 10 trending coins\
        ]\
    except requests.exceptions.RequestException as e:\
        logger.error(f"CoinGecko API error (get_trending_coins): \{e\}")\
        return None\
\
\
def get_coingecko_top_movers_fallback(limit=10, sort_by_index=3, ascending=False):\
    """\
    \uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1090  CoinGecko API \u1082 \u1072 \u1082  \u1079 \u1072 \u1087 \u1072 \u1089 \u1085 \u1086 \u1081  \u1074 \u1072 \u1088 \u1080 \u1072 \u1085 \u1090  \u1076 \u1083 \u1103  \u1087 \u1086 \u1083 \u1091 \u1095 \u1077 \u1085 \u1080 \u1103  \u1083 \u1080 \u1076 \u1077 \u1088 \u1086 \u1074  \u1088 \u1086 \u1089 \u1090 \u1072 /\u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103 .\
\
    Args:\
        limit (int): \uc0\u1052 \u1072 \u1082 \u1089 \u1080 \u1084 \u1072 \u1083 \u1100 \u1085 \u1086 \u1077  \u1082 \u1086 \u1083 \u1080 \u1095 \u1077 \u1089 \u1090 \u1074 \u1086  \u1084 \u1086 \u1085 \u1077 \u1090  \u1074  \u1089 \u1087 \u1080 \u1089 \u1082 \u1077 .\
        sort_by_index (int): \uc0\u1048 \u1085 \u1076 \u1077 \u1082 \u1089  \u1074  \u1082 \u1086 \u1088 \u1090 \u1077 \u1078 \u1077  \u1076 \u1083 \u1103  \u1089 \u1086 \u1088 \u1090 \u1080 \u1088 \u1086 \u1074 \u1082 \u1080  (3 - \u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1080 \u1077  \u1094 \u1077 \u1085 \u1099  \u1079 \u1072  24\u1095  \u1074  \u1087 \u1088 \u1086 \u1094 \u1077 \u1085 \u1090 \u1072 \u1093 ).\
        ascending (bool): \uc0\u1057 \u1086 \u1088 \u1090 \u1080 \u1088 \u1086 \u1074 \u1072 \u1090 \u1100  \u1087 \u1086  \u1074 \u1086 \u1079 \u1088 \u1072 \u1089 \u1090 \u1072 \u1085 \u1080 \u1102  (True \u1076 \u1083 \u1103  \u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103 , False \u1076 \u1083 \u1103  \u1088 \u1086 \u1089 \u1090 \u1072 ).\
\
    Returns:\
        list: \uc0\u1057 \u1087 \u1080 \u1089 \u1086 \u1082  \u1082 \u1086 \u1088 \u1090 \u1077 \u1078 \u1077 \u1081  \u1089  \u1076 \u1072 \u1085 \u1085 \u1099 \u1084 \u1080  \u1086  \u1083 \u1080 \u1076 \u1077 \u1088 \u1072 \u1093  \u1088 \u1086 \u1089 \u1090 \u1072 /\u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103  \u1080 \u1083 \u1080  None \u1074  \u1089 \u1083 \u1091 \u1095 \u1072 \u1077  \u1086 \u1096 \u1080 \u1073 \u1082 \u1080 .\
    """\
    trending_coins = get_trending_coins()  # \uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1084  \u1090 \u1088 \u1077 \u1085 \u1076 \u1086 \u1074 \u1099 \u1077  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  \u1082 \u1072 \u1082  fallback\
    if trending_coins:\
        sorted_coins = sorted(\
            trending_coins,\
            key=lambda x: x[sort_by_index],\
            reverse=not ascending\
        )\
        return sorted_coins[:limit]\
    return None\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  4: \u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082 \u1080  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076  Telegram\
#                       (\uc0\u1050 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099  \u1085 \u1072 \u1095 \u1080 \u1085 \u1072 \u1102 \u1097 \u1080 \u1077 \u1089 \u1103  \u1089  '/')\
# ======================================================================\
\
async def handle_top10_rise(update: Update, context: CallbackContext):\
    """\uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099  '\u1058 \u1086 \u1087  10 \u1088 \u1086 \u1089 \u1090 '."""\
    query = update.callback_query\
    await query.answer()\
\
    top_risers = get_binance_top_movers(\
        sort_by='priceChangePercent', ascending=False)\
\
    if not top_risers:\
        top_risers = get_coingecko_top_movers_fallback(\
            sort_by_index=3, ascending=False)\
        if not top_risers:\
            await query.edit_message_text(TEXTS[context.user_data['language']]['error_fetching_top10_rise'])\
            return\
        else:\
            message = TEXTS[context.user_data['language']\
                            ]['binance_data_unavailable_fallback_rise']\
    else:\
        message = TEXTS[context.user_data['language']]['top10_rise_header']\
\
    for coin in top_risers:\
        coin_id, coin_name, price, change_24h = coin\
        message += (f"\uc0\u55357 \u56520  **\{coin_name\} (\{coin_id\})**: $\{price:.5f\}\\n"\
                    f"\uc0\u55357 \u56520  24h Change: \{change_24h:+.5f\}%\\n\\n")\
\
    # ===  \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1082 \u1083 \u1072 \u1074 \u1080 \u1072 \u1090 \u1091 \u1088 \u1091  \u1075 \u1083 \u1072 \u1074 \u1085 \u1086 \u1075 \u1086  \u1084 \u1077 \u1085 \u1102  ===\
    keyboard = [\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),\
        ],\
    ]\
    reply_markup = InlineKeyboardMarkup(keyboard)\
    # ===  \uc0\u1050 \u1083 \u1072 \u1074 \u1080 \u1072 \u1090 \u1091 \u1088 \u1072  \u1075 \u1083 \u1072 \u1074 \u1085 \u1086 \u1075 \u1086  \u1084 \u1077 \u1085 \u1102  \u1076 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085 \u1072  ===\
\
    # \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  reply_markup\
    await query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)\
\
\
async def handle_top10_fall(update: Update, context: CallbackContext):\
    """\uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099  '\u1058 \u1086 \u1087  10 \u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1103 '."""\
    query = update.callback_query\
    await query.answer()\
\
    top_fallers = get_binance_top_movers(\
        sort_by='priceChangePercent', ascending=True)\
\
    if not top_fallers:\
        top_fallers = get_coingecko_top_movers_fallback(\
            sort_by_index=3, ascending=True)\
        if not top_fallers:\
            await query.edit_message_text(TEXTS[context.user_data['language']]['error_fetching_top10_fall'])\
            return\
        else:\
            message = TEXTS[context.user_data['language']\
                            ]['binance_data_unavailable_fallback_fall']\
    else:\
        message = TEXTS[context.user_data['language']]['top10_fall_header']\
\
    for coin in top_fallers:\
        coin_id, coin_name, price, change_24h = coin\
        message += (f"\uc0\u55357 \u56521  **\{coin_name\} (\{coin_id\})**: $\{price:.4f\}\\n"\
                    f"\uc0\u55357 \u56521  24h Change: \{change_24h:+.4f\}%\\n\\n")\
\
    # ===  \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1082 \u1083 \u1072 \u1074 \u1080 \u1072 \u1090 \u1091 \u1088 \u1091  \u1075 \u1083 \u1072 \u1074 \u1085 \u1086 \u1075 \u1086  \u1084 \u1077 \u1085 \u1102  ===\
    keyboard = [\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),\
        ],\
    ]\
    reply_markup = InlineKeyboardMarkup(keyboard)\
    # ===  \uc0\u1050 \u1083 \u1072 \u1074 \u1080 \u1072 \u1090 \u1091 \u1088 \u1072  \u1075 \u1083 \u1072 \u1074 \u1085 \u1086 \u1075 \u1086  \u1084 \u1077 \u1085 \u1102  \u1076 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085 \u1072  ===\
\
    # \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  reply_markup\
    await query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  5: \u1060 \u1091 \u1085 \u1082 \u1094 \u1080 \u1080  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1086 \u1075 \u1086  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079 \u1072 \
# ======================================================================\
\
def calculate_indicators(prices, high, low, close, volume):\
    """\
    \uc0\u1042 \u1099 \u1095 \u1080 \u1089 \u1083 \u1103 \u1077 \u1090  \u1085 \u1072 \u1073 \u1086 \u1088  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1080 \u1093  \u1080 \u1085 \u1076 \u1080 \u1082 \u1072 \u1090 \u1086 \u1088 \u1086 \u1074 , \u1074 \u1082 \u1083 \u1102 \u1095 \u1072 \u1103  Swing High/Low.\
    """\
    if len(prices) < 50:\
        return None\
\
    obv_values = talib.OBV(np.array(close), np.array(volume))\
\
    period_for_swing = 20  # \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1072 \u1080 \u1074 \u1072 \u1077 \u1084 \u1099 \u1081  \u1087 \u1077 \u1088 \u1080 \u1086 \u1076  \u1076 \u1083 \u1103  \u1086 \u1087 \u1088 \u1077 \u1076 \u1077 \u1083 \u1077 \u1085 \u1080 \u1103  Swing High/Low\
\
    # Swing High \uc0\u1079 \u1072  \u1087 \u1077 \u1088 \u1080 \u1086 \u1076 \
    swing_high = np.max(high[-period_for_swing:]\
                        ) if len(high) >= period_for_swing else None\
    # Swing Low \uc0\u1079 \u1072  \u1087 \u1077 \u1088 \u1080 \u1086 \u1076 \
    swing_low = np.min(low[-period_for_swing:]\
                       ) if len(low) >= period_for_swing else None\
\
    indicators = \{\
        'rsi': talib.RSI(np.array(prices), timeperiod=14)[-1],\
        'macd': talib.MACD(np.array(prices))[0][-1],\
        'signal': talib.MACD(np.array(prices))[1][-1],\
        'ema_30': talib.EMA(np.array(prices), 30)[-1],  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  30\
        'ema_100': talib.EMA(np.array(prices), 100)[-1],  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  100\
        'upper_bb': talib.BBANDS(np.array(prices), timeperiod=20)[0][-1],\
        'lower_bb': talib.BBANDS(np.array(prices), timeperiod=20)[2][-1],\
        'stoch_k': talib.STOCH(np.array(high), np.array(low), np.array(close))[0][-1],\
        'stoch_d': talib.STOCH(np.array(high), np.array(low), np.array(close))[1][-1],\
        'sma_20': talib.SMA(np.array(prices), 20)[-1],\
        'sma_50': talib.SMA(np.array(prices), 50)[-1],\
        'sar': talib.SAR(np.array(high), np.array(low))[-1],\
        'volume': volume[-1],\
        'willr': talib.WILLR(np.array(high), np.array(low), np.array(close), timeperiod=14)[-1],\
        'obv': obv_values[-1],\
        'obv_previous': obv_values[-2] if len(obv_values) > 1 else None,\
        'swing_high': swing_high,  # \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  Swing High \u1074  \u1089 \u1083 \u1086 \u1074 \u1072 \u1088 \u1100  \u1080 \u1085 \u1076 \u1080 \u1082 \u1072 \u1090 \u1086 \u1088 \u1086 \u1074 \
        'swing_low': swing_low,   # \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  Swing Low \u1074  \u1089 \u1083 \u1086 \u1074 \u1072 \u1088 \u1100  \u1080 \u1085 \u1076 \u1080 \u1082 \u1072 \u1090 \u1086 \u1088 \u1086 \u1074 \
    \}\
    return indicators\
\
\
def calculate_support_resistance(prices, period=14):\
    """\
    \uc0\u1042 \u1099 \u1095 \u1080 \u1089 \u1083 \u1103 \u1077 \u1090  \u1091 \u1088 \u1086 \u1074 \u1085 \u1080  \u1087 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1082 \u1080  \u1080  \u1089 \u1086 \u1087 \u1088 \u1086 \u1090 \u1080 \u1074 \u1083 \u1077 \u1085 \u1080 \u1103 .\
    """\
    if len(prices) < period:\
        return None, None\
\
    supports = []\
    resistances = []\
\
    for i in range(period, len(prices)):\
        window = prices[i - period:i]\
        support = np.min(window)\
        resistance = np.max(window)\
        supports.append(support)\
        resistances.append(resistance)\
\
    return supports[-1] if supports else None, resistances[-1] if resistances else None\
\
\
def calculate_adx(high, low, close, period=14):\
    """\
    \uc0\u1042 \u1099 \u1095 \u1080 \u1089 \u1083 \u1103 \u1077 \u1090  \u1080 \u1085 \u1076 \u1077 \u1082 \u1089  \u1085 \u1072 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085 \u1085 \u1086 \u1075 \u1086  \u1076 \u1074 \u1080 \u1078 \u1077 \u1085 \u1080 \u1103  (ADX).\
    """\
    if len(close) < period:\
        return None\
    adx = talib.ADX(np.array(high), np.array(\
        low), np.array(close), timeperiod=period)[-1]\
    return adx\
\
\
def calculate_ichimoku(high, low, close):\
    """\
    \uc0\u1042 \u1099 \u1095 \u1080 \u1089 \u1083 \u1103 \u1077 \u1090  \u1083 \u1080 \u1085 \u1080 \u1080  \u1054 \u1073 \u1083 \u1072 \u1082 \u1072  \u1048 \u1096 \u1080 \u1084 \u1086 \u1082 \u1091 .\
    """\
    if len(close) < 52:  # \uc0\u1052 \u1080 \u1085 \u1080 \u1084 \u1091 \u1084  \u1076 \u1083 \u1103  \u1088 \u1072 \u1089 \u1095 \u1077 \u1090 \u1072  Ichimoku\
        return None, None, None\
    conversion_line = (talib.MAX(np.array(high), timeperiod=9) +\
                       talib.MIN(np.array(low), timeperiod=9)) / 2\
    base_line = (talib.MAX(np.array(high), timeperiod=26) +\
                 talib.MIN(np.array(low), timeperiod=26)) / 2\
    leading_span_a = (conversion_line + base_line) / 2\
    leading_span_b = (talib.MAX(np.array(high), timeperiod=52) +\
                      talib.MIN(np.array(low), timeperiod=52)) / 2\
    return conversion_line[-1], base_line[-1], leading_span_b[-1]\
\
\
# \uc0\u1054 \u1041 \u1053 \u1054 \u1042 \u1051 \u1045 \u1053 \u1054 : \u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085  context\
def determine_trend(ema_30, ema_100, current_price, previous_price, context):\
    """\
    \uc0\u1054 \u1087 \u1088 \u1077 \u1076 \u1077 \u1083 \u1103 \u1077 \u1090  \u1090 \u1088 \u1077 \u1085 \u1076  \u1085 \u1072  \u1086 \u1089 \u1085 \u1086 \u1074 \u1077  \u1089 \u1082 \u1086 \u1083 \u1100 \u1079 \u1103 \u1097 \u1080 \u1093  \u1089 \u1088 \u1077 \u1076 \u1085 \u1080 \u1093  \u1080  \u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1080 \u1103  \u1094 \u1077 \u1085 \u1099 .\
    """\
    trend_text = ""\
    strength_text = ""\
\
    if ema_30 and ema_100:  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  ema_30 \u1080  ema_100\
        if ema_30 > ema_100:  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  ema_30 \u1080  ema_100\
            trend_text += TEXTS[context.user_data['language']\
                                ]['trend_ascending']\
        elif ema_30 < ema_100:  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  ema_30 \u1080  ema_100\
            trend_text += TEXTS[context.user_data['language']\
                                ]['trend_descending']\
        else:\
            trend_text += TEXTS[context.user_data['language']\
                                ]['trend_sideways']\
\
    if current_price and previous_price:\
        price_change = current_price - previous_price\
        if abs(price_change) > 0.05 * current_price:\
            strength_text = TEXTS[context.user_data['language']\
                                  ]['trend_strength_strong']\
        else:\
            strength_text = TEXTS[context.user_data['language']\
                                  ]['trend_strength_weak']\
        if price_change > 0:\
            trend_text += " \uc0\u55357 \u56520 "\
        else:\
            trend_text += " \uc0\u55357 \u56521 "\
\
    return trend_text + strength_text if trend_text else TEXTS[context.user_data['language']]['trend_sideways']\
\
\
def calculate_fibonacci_levels(min_price, max_price):\
    """\
    \uc0\u1056 \u1072 \u1089 \u1089 \u1095 \u1080 \u1090 \u1099 \u1074 \u1072 \u1077 \u1090  \u1091 \u1088 \u1086 \u1074 \u1085 \u1080  \u1082 \u1086 \u1088 \u1088 \u1077 \u1082 \u1094 \u1080 \u1080  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080 .\
    """\
    if max_price < min_price:\
        return \{\}  # \uc0\u1042 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1077 \u1084  \u1087 \u1091 \u1089 \u1090 \u1086 \u1081  \u1089 \u1083 \u1086 \u1074 \u1072 \u1088 \u1100 , \u1077 \u1089 \u1083 \u1080  \u1084 \u1072 \u1082 \u1089 \u1080 \u1084 \u1091 \u1084  \u1084 \u1077 \u1085 \u1100 \u1096 \u1077  \u1084 \u1080 \u1085 \u1080 \u1084 \u1091 \u1084 \u1072 \
\
    diff = max_price - min_price\
    levels = \{\}\
    levels['23.6%'] = max_price - diff * 0.236\
    levels['38.2%'] = max_price - diff * 0.382\
    levels['50.0%'] = max_price - diff * 0.500\
    levels['61.8%'] = max_price - diff * 0.618\
    levels['78.6%'] = max_price - diff * 0.786\
    return levels\
\
\
def get_trading_signal(coin_id: str, interval='1d', context=None):  # \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085 \u1086  context\
    """\
    \uc0\u1054 \u1087 \u1088 \u1077 \u1076 \u1077 \u1083 \u1103 \u1077 \u1090  \u1090 \u1086 \u1088 \u1075 \u1086 \u1074 \u1099 \u1081  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083  \u1085 \u1072  \u1086 \u1089 \u1085 \u1086 \u1074 \u1077  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1080 \u1093  \u1080 \u1085 \u1076 \u1080 \u1082 \u1072 \u1090 \u1086 \u1088 \u1086 \u1074  \u1080  \u1091 \u1088 \u1086 \u1074 \u1085 \u1077 \u1081  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080 .\
    """\
    hist_data = get_historical_data(coin_id, interval)\
    if not hist_data or len(hist_data) < 50:\
        # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1085 \u1086 \u1077  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077  \u1086 \u1073  \u1086 \u1096 \u1080 \u1073 \u1082 \u1077 \
        return TEXTS[context.user_data['language']]['error_invalid_ticker'].format(coin_id), ""\
\
    high = [h for h, _, _, _ in hist_data]\
    low = [l for _, l, _, _ in hist_data]\
    close = [c for _, _, c, _ in hist_data]\
    volume = [v for _, _, _, v in hist_data]\
    prices = close\
\
    indicators = calculate_indicators(prices, high, low, close, volume)\
    support, resistance = calculate_support_resistance(prices)\
    # === \uc0\u1056 \u1072 \u1089 \u1095 \u1077 \u1090  \u1091 \u1088 \u1086 \u1074 \u1085 \u1077 \u1081  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  ===\
    # \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1072 \u1080 \u1074 \u1072 \u1077 \u1084 \u1099 \u1081  \u1087 \u1077 \u1088 \u1080 \u1086 \u1076  \u1076 \u1083 \u1103  Swing High/Low \u1076 \u1083 \u1103  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080 \
    period_for_fibonacci_swing = 30\
    swing_high_fib = np.max(high[-period_for_fibonacci_swing:]\
                            ) if len(high) >= period_for_fibonacci_swing else None\
    swing_low_fib = np.min(low[-period_for_fibonacci_swing:]\
                           ) if len(low) >= period_for_fibonacci_swing else None\
    fibonacci_levels = \{\}\
    if swing_high_fib and swing_low_fib:\
        fibonacci_levels = calculate_fibonacci_levels(\
            swing_low_fib, swing_high_fib)\
    # === \uc0\u1050 \u1086 \u1085 \u1077 \u1094  \u1088 \u1072 \u1089 \u1095 \u1077 \u1090 \u1072  \u1091 \u1088 \u1086 \u1074 \u1085 \u1077 \u1081  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  ===\
\
    buy_signals = sell_signals = 0\
\
    # --- \uc0\u1057 \u1091 \u1097 \u1077 \u1089 \u1090 \u1074 \u1091 \u1102 \u1097 \u1080 \u1077  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1099  (\u1089  \u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1085 \u1099 \u1084 \u1080  \u1087 \u1086 \u1088 \u1086 \u1075 \u1072 \u1084 \u1080  RSI/Stochastic) ---\
    if close[-1] <= indicators['lower_bb']:\
        buy_signals += 1\
    elif close[-1] >= indicators['upper_bb']:\
        sell_signals += 1\
    if indicators['stoch_k'] < 25:  # Stochastic K \uc0\u1087 \u1077 \u1088 \u1077 \u1087 \u1088 \u1086 \u1076 \u1072 \u1085  (\u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  25)\
        buy_signals += 1\
    # Stochastic K \uc0\u1087 \u1077 \u1088 \u1077 \u1082 \u1091 \u1087 \u1083 \u1077 \u1085  (\u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  75)\
    elif indicators['stoch_k'] > 75:\
        sell_signals += 1\
    if indicators['sma_20'] > indicators['sma_50']:\
        buy_signals += 1\
    elif indicators['sma_20'] < indicators['sma_50']:\
        sell_signals += 1\
    if indicators['volume'] > np.mean(volume[-5:]) * 1.5:\
        if close[-1] > close[-2]:\
            buy_signals += 1\
        else:\
            sell_signals += 1\
    if close[-1] > indicators['sar']:\
        buy_signals += 1\
    else:\
        sell_signals += 1\
    if support and resistance:\
        if close[-1] <= support * 1.005:\
            buy_signals += 1\
        elif close[-1] >= resistance * 0.995:\
            sell_signals += 1\
    if indicators['rsi'] > 65:  # RSI \uc0\u1087 \u1077 \u1088 \u1077 \u1082 \u1091 \u1087 \u1083 \u1077 \u1085  (\u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  65)\
        sell_signals += 1\
    elif indicators['rsi'] < 35:  # RSI \uc0\u1087 \u1077 \u1088 \u1077 \u1087 \u1088 \u1086 \u1076 \u1072 \u1085  (\u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  35)\
        buy_signals += 1\
    if indicators['macd'] > indicators['signal']:\
        buy_signals += 1\
    elif indicators['macd'] < indicators['signal']:\
        sell_signals += 1\
    if indicators['ema_30'] > indicators['ema_100']:  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  ema_30 \u1080  ema_100\
        buy_signals += 1\
    elif indicators['ema_30'] < indicators['ema_100']:  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  ema_30 \u1080  ema_100\
        sell_signals += 1\
    if indicators['willr'] < -80:\
        buy_signals += 1\
    elif indicators['willr'] > -20:\
        sell_signals += 1\
\
    # --- \uc0\u1057 \u1080 \u1075 \u1085 \u1072 \u1083 \u1099  \u1085 \u1072  \u1086 \u1089 \u1085 \u1086 \u1074 \u1077  OBV ---\
    obv = indicators['obv']\
    previous_obv = indicators.get('obv_previous')\
\
    if previous_obv is not None:\
        if obv > previous_obv:\
            buy_signals += 1\
        elif obv < previous_obv:\
            sell_signals += 1\
    # --- \uc0\u1050 \u1054 \u1053 \u1045 \u1062  \u1041 \u1051 \u1054 \u1050 \u1040  \u1044 \u1051 \u1071  OBV\
\
    # --- \uc0\u1053 \u1086 \u1074 \u1099 \u1077  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1099  ---\
    # ADX\
    adx = calculate_adx(high, low, close)\
    if adx and adx > 25:\
        buy_signals += 1\
\
    # Ichimoku\
    conversion_line, base_line, leading_span_b = calculate_ichimoku(\
        high, low, close)\
    if conversion_line and base_line and leading_span_b:\
        if close[-1] > conversion_line and close[-1] > base_line:\
            buy_signals += 1\
        elif close[-1] < conversion_line and close[-1] < base_line:\
            sell_signals += 1\
\
    # --- \uc0\u1057 \u1080 \u1075 \u1085 \u1072 \u1083 \u1099  \u1085 \u1072  \u1086 \u1089 \u1085 \u1086 \u1074 \u1077  \u1091 \u1088 \u1086 \u1074 \u1085 \u1077 \u1081  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  ---\
    if fibonacci_levels:\
        current_price = close[-1]\
        for level_name, level_value in fibonacci_levels.items():\
            # \uc0\u1056 \u1072 \u1089 \u1089 \u1084 \u1086 \u1090 \u1088 \u1080 \u1084  \u1087 \u1077 \u1088 \u1074 \u1099 \u1077  3 \u1091 \u1088 \u1086 \u1074 \u1085 \u1103  \u1082 \u1072 \u1082  \u1085 \u1072 \u1080 \u1073 \u1086 \u1083 \u1077 \u1077  \u1079 \u1085 \u1072 \u1095 \u1080 \u1084 \u1099 \u1077  \u1087 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1082 \u1080 /\u1089 \u1086 \u1087 \u1088 \u1086 \u1090 \u1080 \u1074 \u1083 \u1077 \u1085 \u1080 \u1103 \
            if level_name in ['23.6%', '38.2%', '50.0%']:\
                # \uc0\u1062 \u1077 \u1085 \u1072  \u1074 \u1073 \u1083 \u1080 \u1079 \u1080  \u1091 \u1088 \u1086 \u1074 \u1085 \u1103  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  (\u1076 \u1086 \u1087 \u1091 \u1089 \u1082  0.5%)\
                if current_price >= level_value * 0.995 and current_price <= level_value * 1.005:\
                    # \uc0\u1059 \u1088 \u1086 \u1074 \u1077 \u1085 \u1100  \u1085 \u1072 \u1093 \u1086 \u1076 \u1080 \u1090 \u1089 \u1103  \u1084 \u1077 \u1078 \u1076 \u1091  Swing High \u1080  Swing Low\
                    if level_value < swing_high_fib and level_value > swing_low_fib:\
                        if current_price < level_value:  # \uc0\u1062 \u1077 \u1085 \u1072  \u1085 \u1080 \u1078 \u1077  \u1091 \u1088 \u1086 \u1074 \u1085 \u1103  - \u1087 \u1086 \u1090 \u1077 \u1085 \u1094 \u1080 \u1072 \u1083 \u1100 \u1085 \u1086 \u1077  \u1089 \u1086 \u1087 \u1088 \u1086 \u1090 \u1080 \u1074 \u1083 \u1077 \u1085 \u1080 \u1077 \
                            sell_signals += 1\
                        else:  # \uc0\u1062 \u1077 \u1085 \u1072  \u1074 \u1099 \u1096 \u1077  \u1091 \u1088 \u1086 \u1074 \u1085 \u1103  - \u1087 \u1086 \u1090 \u1077 \u1085 \u1094 \u1080 \u1072 \u1083 \u1100 \u1085 \u1072 \u1103  \u1087 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1082 \u1072 \
                            buy_signals += 1\
    # --- \uc0\u1050 \u1054 \u1053 \u1045 \u1062  \u1041 \u1051 \u1054 \u1050 \u1040  \u1057 \u1048 \u1043 \u1053 \u1040 \u1051 \u1054 \u1042  \u1060 \u1048 \u1041 \u1054 \u1053 \u1040 \u1063 \u1063 \u1048  ---\
\
    signal_text = TEXTS[context.user_data['language']]['signal_buy'] if buy_signals > sell_signals else TEXTS[context.user_data['language']\
                                                                                                              ]['signal_sell'] if sell_signals > buy_signals else TEXTS[context.user_data['language']]['signal_hold']\
\
    trend = determine_trend(\
        indicators['ema_30'],  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  ema_30\
        indicators['ema_100'],  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  ema_100\
        close[-1],\
        close[-2] if len(close) > 1 else None,\
        context  # \uc0\u1044 \u1054 \u1041 \u1040 \u1042 \u1051 \u1045 \u1053 \u1054 : \u1055 \u1077 \u1088 \u1077 \u1076 \u1072 \u1095 \u1072  context\
    )\
\
    return signal_text, trend, fibonacci_levels  # \uc0\u1042 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1077 \u1084  fibonacci_levels\
\
\
def get_historical_data(coin_id: str, interval='1d'):\
    """\
    \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1090  \u1080 \u1089 \u1090 \u1086 \u1088 \u1080 \u1095 \u1077 \u1089 \u1082 \u1080 \u1077  \u1076 \u1072 \u1085 \u1085 \u1099 \u1077  \u1094 \u1077 \u1085 \u1099  \u1076 \u1083 \u1103  \u1084 \u1086 \u1085 \u1077 \u1090 \u1099  \u1089  Binance API.\
    """\
    try:\
        if interval == '24h':  # \uc0\u1048 \u1089 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085 \u1080 \u1077 : \u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1100  '1d' \u1076 \u1083 \u1103  24h\
            binance_interval = '1d'\
        elif interval == '8h':\
            binance_interval = '8h'\
        elif interval == '4h':\
            binance_interval = '4h'\
        elif interval == '12h':\
            binance_interval = '12h'\
        elif interval == '1h':\
            binance_interval = '1h'\
        else:\
            binance_interval = interval\
\
        url = f"https://api.binance.com/api/v3/klines?symbol=\{coin_id.upper()\}USDT&interval=\{binance_interval\}&limit=200"\
        response = requests.get(url)\
        response.raise_for_status()\
        hist_data_json = response.json()\
        return [\
            (float(c[2]),  # high\
             float(c[3]),  # low\
             float(c[4]),  # close\
             float(c[5]))  # volume\
            for c in hist_data_json\
        ]\
    except requests.exceptions.RequestException as e:\
        logger.error(\
            f"Historical data error (get_historical_data for \{coin_id\}, interval \{interval\}): \{e\}")\
        return None\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  6: \u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082 \u1080  \u1090 \u1077 \u1082 \u1089 \u1090 \u1086 \u1074 \u1099 \u1093  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1081  Telegram\
#                       (\uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1072  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1100 \u1089 \u1082 \u1086 \u1075 \u1086  \u1074 \u1074 \u1086 \u1076 \u1072  \u1090 \u1077 \u1082 \u1089 \u1090 \u1072 )\
# ======================================================================\
\
async def handle_text(update: Update, context: CallbackContext):\
    """\
    \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1072 \u1090 \u1099 \u1074 \u1072 \u1077 \u1090  \u1090 \u1077 \u1082 \u1089 \u1090 \u1086 \u1074 \u1099 \u1077  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1103  \u1086 \u1090  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103 .\
    \uc0\u1054 \u1087 \u1088 \u1077 \u1076 \u1077 \u1083 \u1103 \u1077 \u1090 , \u1103 \u1074 \u1083 \u1103 \u1077 \u1090 \u1089 \u1103  \u1083 \u1080  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077  \u1079 \u1072 \u1087 \u1088 \u1086 \u1089 \u1086 \u1084  \u1094 \u1077 \u1085 \u1099  \u1080 \u1083 \u1080  \u1079 \u1072 \u1087 \u1088 \u1086 \u1089 \u1086 \u1084  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1086 \u1075 \u1086  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079 \u1072 .\
    """\
    text = update.message.text.strip().upper()\
    parts = text.split()\
\
    if len(parts) == 1:  # \uc0\u1054 \u1076 \u1080 \u1085 \u1086 \u1095 \u1085 \u1099 \u1081  \u1090 \u1080 \u1082 \u1077 \u1088  \u1076 \u1083 \u1103  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1086 \u1075 \u1086  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079 \u1072 \
        coin_id = text\
        price_data = get_binance_price(coin_id)\
\
        if not price_data:\
            await update.message.reply_text(TEXTS[context.user_data['language']]['error_fetching_data'])\
            return\
\
        price = float(price_data['lastPrice'])\
        change_24h = float(price_data['priceChangePercent'])\
\
        # \uc0\u1055 \u1077 \u1088 \u1077 \u1076 \u1072 \u1077 \u1084  context \u1074  get_trading_signal\
        signal_info = get_trading_signal(coin_id, context=context)\
\
        # \uc0\u1087 \u1088 \u1086 \u1074 \u1077 \u1088 \u1103 \u1077 \u1084 , \u1095 \u1090 \u1086  \u1074 \u1077 \u1088 \u1085 \u1091 \u1083 \u1086 \u1089 \u1100  3 \u1079 \u1085 \u1072 \u1095 \u1077 \u1085 \u1080 \u1103 \
        if isinstance(signal_info, tuple) and len(signal_info) == 3:\
            # \uc0\u1088 \u1072 \u1089 \u1087 \u1072 \u1082 \u1086 \u1074 \u1099 \u1074 \u1072 \u1077 \u1084  \u1079 \u1085 \u1072 \u1095 \u1077 \u1085 \u1080 \u1103 , \u1077 \u1089 \u1083 \u1080  \u1080 \u1093  3\
            signal_text, trend_text, fibonacci_levels = signal_info\
        else:  # \uc0\u1077 \u1089 \u1083 \u1080  \u1074 \u1077 \u1088 \u1085 \u1091 \u1083 \u1086 \u1089 \u1100  \u1085 \u1077  3 \u1079 \u1085 \u1072 \u1095 \u1077 \u1085 \u1080 \u1103  (\u1086 \u1096 \u1080 \u1073 \u1082 \u1072 )\
            signal_text, trend_text = signal_info if isinstance(signal_info, tuple) else (\
                # \uc0\u1086 \u1073 \u1088 \u1072 \u1073 \u1072 \u1090 \u1099 \u1074 \u1072 \u1077 \u1084 , \u1077 \u1089 \u1083 \u1080  \u1074 \u1077 \u1088 \u1085 \u1091 \u1083 \u1086 \u1089 \u1100  2 \u1080 \u1083 \u1080  \u1095 \u1090 \u1086 -\u1090 \u1086  \u1076 \u1088 \u1091 \u1075 \u1086 \u1077 \
                TEXTS[context.user_data['language']]['error_fetching_data'], "")\
            fibonacci_levels = \{\}  # \uc0\u1074  \u1089 \u1083 \u1091 \u1095 \u1072 \u1077  \u1086 \u1096 \u1080 \u1073 \u1082 \u1080  \u1091 \u1088 \u1086 \u1074 \u1085 \u1080  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  \u1076 \u1077 \u1083 \u1072 \u1077 \u1084  \u1087 \u1091 \u1089 \u1090 \u1099 \u1084 \u1080 \
\
        # ===  \uc0\u1054 \u1087 \u1088 \u1077 \u1076 \u1077 \u1083 \u1077 \u1085 \u1080 \u1077  \u1089 \u1080 \u1083 \u1099  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1072  \u1080  \u1076 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085 \u1080 \u1077  \u1089 \u1090 \u1088 \u1077 \u1083 \u1086 \u1082  (\u1076 \u1083 \u1103  24h \u1090 \u1072 \u1081 \u1084 \u1092 \u1088 \u1077 \u1081 \u1084 \u1072 ) ===\
        signal_strength_arrows = ""\
        buy_signals = 0  # \uc0\u1048 \u1085 \u1080 \u1094 \u1080 \u1072 \u1083 \u1080 \u1079 \u1072 \u1094 \u1080 \u1103  \u1076 \u1083 \u1103  \u1076 \u1086 \u1089 \u1090 \u1091 \u1087 \u1072  \u1074  \u1101 \u1090 \u1086 \u1084  \u1089 \u1082 \u1086 \u1091 \u1087 \u1077 \
        sell_signals = 0  # \uc0\u1048 \u1085 \u1080 \u1094 \u1080 \u1072 \u1083 \u1080 \u1079 \u1072 \u1094 \u1080 \u1103  \u1076 \u1083 \u1103  \u1076 \u1086 \u1089 \u1090 \u1091 \u1087 \u1072  \u1074  \u1101 \u1090 \u1086 \u1084  \u1089 \u1082 \u1086 \u1091 \u1087 \u1077 \
        if signal_text == TEXTS[context.user_data['language']]['signal_buy']:\
            buy_signals, sell_signals = get_signal_counts_for_arrows(\
                coin_id, context=context)  # \uc0\u1055 \u1077 \u1088 \u1077 \u1076 \u1072 \u1077 \u1084  context\
            if buy_signals - sell_signals >= 3:  # \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1072 \u1080 \u1074 \u1072 \u1077 \u1084 \u1099 \u1081  \u1087 \u1086 \u1088 \u1086 \u1075  \u1076 \u1083 \u1103  "\u1089 \u1080 \u1083 \u1100 \u1085 \u1086 \u1075 \u1086 " \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1072 \
                # 3 \uc0\u1089 \u1090 \u1088 \u1077 \u1083 \u1082 \u1080  \u1074 \u1074 \u1077 \u1088 \u1093  \u1076 \u1083 \u1103  \u1089 \u1080 \u1083 \u1100 \u1085 \u1086 \u1075 \u1086  BUY (\u1079 \u1072 \u1084 \u1077 \u1085 \u1072  \u1082 \u1088 \u1091 \u1078 \u1082 \u1086 \u1074 )\
                signal_strength_arrows = "\uc0\u11014 \u65039 \u11014 \u65039 \u11014 \u65039  "\
        elif signal_text == TEXTS[context.user_data['language']]['signal_sell']:\
            buy_signals, sell_signals = get_signal_counts_for_arrows(\
                coin_id, context=context)  # \uc0\u1055 \u1077 \u1088 \u1077 \u1076 \u1072 \u1077 \u1084  context\
            if sell_signals - buy_signals >= 3:  # \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1072 \u1080 \u1074 \u1072 \u1077 \u1084 \u1099 \u1081  \u1087 \u1086 \u1088 \u1086 \u1075  \u1076 \u1083 \u1103  "\u1089 \u1080 \u1083 \u1100 \u1085 \u1086 \u1075 \u1086 " \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1072 \
                # 3 \uc0\u1089 \u1090 \u1088 \u1077 \u1083 \u1082 \u1080  \u1074 \u1085 \u1080 \u1079  \u1076 \u1083 \u1103  \u1089 \u1080 \u1083 \u1100 \u1085 \u1086 \u1075 \u1086  SELL (\u1079 \u1072 \u1084 \u1077 \u1085 \u1072  \u1082 \u1088 \u1091 \u1078 \u1082 \u1086 \u1074 )\
                signal_strength_arrows = "\uc0\u11015 \u65039 \u11015 \u65039 \u11015 \u65039  "\
        # ===  \uc0\u1050 \u1054 \u1053 \u1045 \u1062  \u1041 \u1051 \u1054 \u1050 \u1040  \u1057 \u1058 \u1056 \u1045 \u1051 \u1054 \u1050  ===\
\
        message = (TEXTS[context.user_data['language']]['price_coin'].format(coin_id, price) +\
                   TEXTS[context.user_data['language']]['change_24h'].format(change_24h) +\
                   TEXTS[context.user_data['language']]['signal_24h'].format(signal_strength_arrows + signal_text) +\
                   TEXTS[context.user_data['language']]['trend_24h'].format(trend_text))\
\
        # \uc0\u1041 \u1083 \u1086 \u1082  \u1089  \u1091 \u1088 \u1086 \u1074 \u1085 \u1103 \u1084 \u1080  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  \u1059 \u1044 \u1040 \u1051 \u1045 \u1053 \
\
        keyboard = [\
            [\
                InlineKeyboardButton(\
                    TEXTS[context.user_data['language']]['button_1h'], callback_data=f"\{coin_id\}_1h"),\
                InlineKeyboardButton(\
                    TEXTS[context.user_data['language']]['button_4h'], callback_data=f"\{coin_id\}_4h"),\
            ],\
            [\
                InlineKeyboardButton(\
                    TEXTS[context.user_data['language']]['button_12h'], callback_data=f"\{coin_id\}_12h"),\
                InlineKeyboardButton(\
                    TEXTS[context.user_data['language']]['back_button'], callback_data=f"\{coin_id\}_back"),\
            ]\
        ]\
        reply_markup = InlineKeyboardMarkup(keyboard)\
\
        await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)\
\
    # \uc0\u1047 \u1072 \u1087 \u1088 \u1086 \u1089  \u1094 \u1077 \u1085 \u1099  \u1074  USDT (\u1082 \u1086 \u1083 \u1080 \u1095 \u1077 \u1089 \u1090 \u1074 \u1086  COIN USDT)\
    elif len(parts) == 2 and parts[1].upper() == "USDT":\
        try:\
            amount_str, coin_symbol_original = parts\
            amount = float(amount_str)\
            coin_symbol = coin_symbol_original.upper()\
\
            # === === ===  \uc0\u1048 \u1057 \u1055 \u1054 \u1051 \u1068 \u1047 \u1059 \u1045 \u1052  COINGECKO \u1044 \u1051 \u1071  \u1062 \u1045 \u1053  USDT \u1055 \u1040 \u1056   === === ===\
            coingecko_coin_id = get_coingecko_coin_id_by_symbol(\
                coin_symbol)  # \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1084  CoinGecko ID \u1087 \u1086  \u1089 \u1080 \u1084 \u1074 \u1086 \u1083 \u1091 \
\
            if coingecko_coin_id:\
                # \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1084  \u1094 \u1077 \u1085 \u1091  \u1095 \u1077 \u1088 \u1077 \u1079  CoinGecko\
                price_usd = get_coingecko_price(coingecko_coin_id, 'usd')\
                if price_usd is not None:\
                    calculated_value = amount * price_usd\
                    message = TEXTS[context.user_data['language']]['price_in_usdt'].format(\
                        calculated_value)  # \uc0\u1060 \u1086 \u1088 \u1084 \u1072 \u1090 \u1080 \u1088 \u1091 \u1077 \u1084  \u1089  8 \u1079 \u1085 \u1072 \u1082 \u1072 \u1084 \u1080  \u1087 \u1086 \u1089 \u1083 \u1077  \u1079 \u1072 \u1087 \u1103 \u1090 \u1086 \u1081 \
                    await update.message.reply_text(f"\uc0\u55357 \u56496  \{message\}")\
                else:\
                    # \uc0\u1057 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077  \u1086 \u1073  \u1086 \u1096 \u1080 \u1073 \u1082 \u1077 , \u1077 \u1089 \u1083 \u1080  \u1094 \u1077 \u1085 \u1072  \u1085 \u1077  \u1087 \u1086 \u1083 \u1091 \u1095 \u1077 \u1085 \u1072  \u1089  CoinGecko\
                    await update.message.reply_text(TEXTS[context.user_data['language']]['error_fetching_price_usdt'].format(coin_symbol))\
            else:\
                # \uc0\u1057 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077  \u1086 \u1073  \u1086 \u1096 \u1080 \u1073 \u1082 \u1077 , \u1077 \u1089 \u1083 \u1080  CoinGecko ID \u1085 \u1077  \u1085 \u1072 \u1081 \u1076 \u1077 \u1085 \
                await update.message.reply_text(TEXTS[context.user_data['language']]['error_invalid_ticker'].format(coin_symbol))\
            # === === ===  \uc0\u1050 \u1054 \u1053 \u1045 \u1062  \u1041 \u1051 \u1054 \u1050 \u1040  COINGECKO  === === ===\
\
        except ValueError:\
            await update.message.reply_text(TEXTS[context.user_data['language']]['invalid_input_amount_coin_coin'])\
\
    elif len(parts) == 3:  # \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1072  "\u1082 \u1086 \u1083 \u1080 \u1095 \u1077 \u1089 \u1090 \u1074 \u1086  COIN1 COIN2" \u1076 \u1083 \u1103  \u1083 \u1102 \u1073 \u1086 \u1075 \u1086  \u1090 \u1080 \u1082 \u1077 \u1088 \u1072 \
        try:\
            amount = float(parts[0])\
            coin1_id = parts[1]\
            coin2_id = parts[2]\
\
            # \uc0\u1055 \u1086 \u1087 \u1099 \u1090 \u1082 \u1072  \u1087 \u1086 \u1083 \u1091 \u1095 \u1080 \u1090 \u1100  \u1087 \u1088 \u1103 \u1084 \u1091 \u1102  \u1094 \u1077 \u1085 \u1091  \u1089  Binance (\u1082 \u1072 \u1082  \u1073 \u1099 \u1083 \u1086  \u1088 \u1072 \u1085 \u1100 \u1096 \u1077  \u1076 \u1083 \u1103  \u1082 \u1088 \u1080 \u1087 \u1090 \u1086 -\u1082 \u1088 \u1080 \u1087 \u1090 \u1086  \u1087 \u1072 \u1088 )\
            direct_price = get_binance_price_direct(coin1_id, coin2_id)\
\
            if direct_price:\
                # \uc0\u1045 \u1089 \u1083 \u1080  \u1087 \u1088 \u1103 \u1084 \u1072 \u1103  \u1094 \u1077 \u1085 \u1072  \u1077 \u1089 \u1090 \u1100  \u1085 \u1072  Binance, \u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1084  \u1077 \u1077  (\u1082 \u1072 \u1082  \u1080  \u1088 \u1072 \u1085 \u1100 \u1096 \u1077  \u1076 \u1083 \u1103  \u1082 \u1088 \u1080 \u1087 \u1090 \u1086 -\u1082 \u1088 \u1080 \u1087 \u1090 \u1086  \u1087 \u1072 \u1088 )\
                calculated_value = amount * direct_price\
                message = TEXTS[context.user_data['language']]['price_in_crypto'].format(\
                    calculated_value, coin2_id.upper())\
                await update.message.reply_text(f"\uc0\u55357 \u56496  \{message\}")\
            else:\
                # \uc0\u1045 \u1089 \u1083 \u1080  \u1087 \u1088 \u1103 \u1084 \u1086 \u1081  \u1087 \u1072 \u1088 \u1099  \u1085 \u1077 \u1090  \u1085 \u1072  Binance, \u1087 \u1099 \u1090 \u1072 \u1077 \u1084 \u1089 \u1103  \u1088 \u1072 \u1089 \u1089 \u1095 \u1080 \u1090 \u1072 \u1090 \u1100  \u1095 \u1077 \u1088 \u1077 \u1079  USDT (\u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1084  Binance \u1094 \u1077 \u1085 \u1099  \u1076 \u1083 \u1103  \u1082 \u1088 \u1080 \u1087 \u1090 \u1086 -\u1082 \u1088 \u1080 \u1087 \u1090 \u1086  \u1087 \u1072 \u1088 , \u1082 \u1072 \u1082  \u1080  \u1088 \u1072 \u1085 \u1100 \u1096 \u1077 )\
                price_coin1_usdt_data = get_binance_price(coin1_id)\
                price_coin2_usdt_data = get_binance_price(coin2_id)\
\
                if price_coin1_usdt_data and price_coin2_usdt_data:\
                    # \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1084  \u1094 \u1077 \u1085 \u1099  COIN1/USDT \u1080  COIN2/USDT \u1089  Binance\
                    price_coin1_usdt = float(\
                        price_coin1_usdt_data['lastPrice'])\
                    price_coin2_usdt = float(\
                        price_coin2_usdt_data['lastPrice'])\
\
                    # \uc0\u1056 \u1072 \u1089 \u1089 \u1095 \u1080 \u1090 \u1099 \u1074 \u1072 \u1077 \u1084  \u1089 \u1090 \u1086 \u1080 \u1084 \u1086 \u1089 \u1090 \u1100  COIN1 \u1074  COIN2 \u1095 \u1077 \u1088 \u1077 \u1079  USDT \u1082 \u1072 \u1082  \u1087 \u1086 \u1089 \u1088 \u1077 \u1076 \u1085 \u1080 \u1082 \u1072  (\u1080 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1084  Binance \u1094 \u1077 \u1085 \u1099 )\
                    calculated_value = (\
                        amount * price_coin1_usdt) / price_coin2_usdt\
                    message = TEXTS[context.user_data['language']]['price_in_crypto'].format(\
                        calculated_value, coin2_id.upper())\
                    await update.message.reply_text(f"\uc0\u55357 \u56496  \{message\}")\
                else:\
                    # \uc0\u1045 \u1089 \u1083 \u1080  \u1085 \u1077  \u1091 \u1076 \u1072 \u1083 \u1086 \u1089 \u1100  \u1087 \u1086 \u1083 \u1091 \u1095 \u1080 \u1090 \u1100  \u1094 \u1077 \u1085 \u1091  \u1095 \u1077 \u1088 \u1077 \u1079  USDT \u1085 \u1072  Binance, \u1074 \u1099 \u1074 \u1086 \u1076 \u1080 \u1084  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077  \u1086 \u1073  \u1086 \u1096 \u1080 \u1073 \u1082 \u1077 \
                    await update.message.reply_text(\
                        TEXTS[context.user_data['language']]['error_fetching_price_crypto'].format(coin1_id, coin2_id))\
\
        except ValueError:\
            await update.message.reply_text(TEXTS[context.user_data['language']]['invalid_input_amount_coin_coin'])\
        except IndexError:\
            await update.message.reply_text(TEXTS[context.user_data['language']]['invalid_input_amount_coin_coin_index_error'])\
\
    else:  # \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1072  \u1086 \u1096 \u1080 \u1073 \u1086 \u1082  \u1074 \u1074 \u1086 \u1076 \u1072 \
        await update.message.reply_text(TEXTS[context.user_data['language']]['error_fetching_data'])\
\
\
async def handle_timeframe_data(update: Update, context: CallbackContext):\
    """\
    \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1072 \u1090 \u1099 \u1074 \u1072 \u1077 \u1090  \u1079 \u1072 \u1087 \u1088 \u1086 \u1089 \u1099  \u1085 \u1072  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1080 \u1081  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079  \u1076 \u1083 \u1103  \u1088 \u1072 \u1079 \u1085 \u1099 \u1093  \u1090 \u1072 \u1081 \u1084 \u1092 \u1088 \u1077 \u1081 \u1084 \u1086 \u1074  (\u1087 \u1086  \u1085 \u1072 \u1078 \u1072 \u1090 \u1080 \u1102  \u1082 \u1085 \u1086 \u1087 \u1086 \u1082 ).\
    """\
    query = update.callback_query\
    await query.answer()\
\
    data = query.data.split("_")\
    coin_id = data[0]\
    interval = data[1]\
\
    if interval == 'back':\
        await query.edit_message_reply_markup(reply_markup=None)\
        return\
\
    hist_data = get_historical_data(coin_id, interval)\
    if not hist_data or len(hist_data) < 2:\
        await query.edit_message_text(TEXTS[context.user_data['language']]['not_enough_historical_data'])\
        return\
\
    ### ====================  \uc0\u1041 \u1051 \u1054 \u1050  \u1053 \u1040 \u1057 \u1058 \u1056 \u1054 \u1049 \u1050 \u1048  \u1048  \u1055 \u1054 \u1050 \u1040 \u1047 \u1040  \u1055 \u1056 \u1054 \u1062 \u1045 \u1053 \u1058 \u1054 \u1042  (\u1053 \u1040 \u1063 \u1040 \u1051 \u1054 ) ==================== ###\
    interval_change_percent = 0.0\
\
    if len(hist_data) >= 2:\
        first_price = hist_data[1][2]\
        last_price = hist_data[0][2]\
        interval_change_percent = (\
            (last_price - first_price) / first_price) * 100\
\
    ### ====================  \uc0\u1041 \u1051 \u1054 \u1050  \u1053 \u1040 \u1057 \u1058 \u1056 \u1054 \u1049 \u1050 \u1048  \u1048  \u1055 \u1054 \u1050 \u1040 \u1047 \u1040  \u1055 \u1056 \u1054 \u1062 \u1045 \u1053 \u1058 \u1054 \u1042  (\u1050 \u1054 \u1053 \u1045 \u1062 ) ==================== ###\
\
    signal_text, trend_text, fibonacci_levels = get_trading_signal(\
        coin_id, interval, context=context)  # \uc0\u1055 \u1077 \u1088 \u1077 \u1076 \u1072 \u1077 \u1084  context\
    # \uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1084  Binance \u1076 \u1083 \u1103  \u1090 \u1077 \u1082 \u1091 \u1097 \u1077 \u1081  \u1094 \u1077 \u1085 \u1099  \u1074  \u1090 \u1077 \u1093 \u1085 \u1080 \u1095 \u1077 \u1089 \u1082 \u1086 \u1084  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079 \u1077  (\u1084 \u1086 \u1078 \u1085 \u1086  \u1080 \u1079 \u1084 \u1077 \u1085 \u1080 \u1090 \u1100  \u1085 \u1072  CoinGecko, \u1077 \u1089 \u1083 \u1080  \u1085 \u1091 \u1078 \u1085 \u1086 )\
    price_data = get_binance_price(coin_id)\
\
    if not price_data:\
        await query.edit_message_text(TEXTS[context.user_data['language']]['error_fetching_timeframe_data'])\
        return\
\
    price = float(price_data['lastPrice'])\
    high = [h[0] for h in hist_data]\
    low = [l[1] for l in hist_data]\
    close_prices = [c[2] for c in hist_data]\
    volume = [v[3] for v in hist_data]\
    prices = close_prices  # \uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1084  close_prices \u1082 \u1072 \u1082  'prices' \u1076 \u1083 \u1103  \u1080 \u1085 \u1076 \u1080 \u1082 \u1072 \u1090 \u1086 \u1088 \u1086 \u1074 \
\
    # \uc0\u1048 \u1089 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085 \u1085 \u1099 \u1081  \u1074 \u1099 \u1079 \u1086 \u1074  calculate_indicators:\
    # \uc0\u1055 \u1077 \u1088 \u1077 \u1076 \u1072 \u1077 \u1084  close_prices \u1082 \u1072 \u1082  'close'\
    indicators = calculate_indicators(prices, high, low, close_prices, volume)\
\
    # ===  \uc0\u1056 \u1072 \u1089 \u1095 \u1077 \u1090  \u1091 \u1088 \u1086 \u1074 \u1085 \u1077 \u1081  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080   ===\
    # \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1072 \u1080 \u1074 \u1072 \u1077 \u1084 \u1099 \u1081  \u1087 \u1077 \u1088 \u1080 \u1086 \u1076  \u1076 \u1083 \u1103  Swing High/Low \u1076 \u1083 \u1103  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080 \
    period_for_fibonacci_swing = 30\
    swing_high_fib = np.max(high[-period_for_fibonacci_swing:]\
                            ) if len(high) >= period_for_fibonacci_swing else None\
    swing_low_fib = np.min(low[-period_for_fibonacci_swing:]\
                           ) if len(low) >= period_for_fibonacci_swing else None\
\
    # ===  \uc0\u1054 \u1087 \u1088 \u1077 \u1076 \u1077 \u1083 \u1077 \u1085 \u1080 \u1077  \u1089 \u1080 \u1083 \u1099  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1072  \u1080  \u1076 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085 \u1080 \u1077  \u1089 \u1090 \u1088 \u1077 \u1083 \u1086 \u1082  ===\
    signal_strength_arrows = ""\
    buy_signals = 0  # \uc0\u1048 \u1085 \u1080 \u1094 \u1080 \u1072 \u1083 \u1080 \u1079 \u1072 \u1094 \u1080 \u1103  \u1076 \u1083 \u1103  \u1076 \u1086 \u1089 \u1090 \u1091 \u1087 \u1072  \u1074  \u1101 \u1090 \u1086 \u1084  \u1089 \u1082 \u1086 \u1091 \u1087 \u1077 \
    sell_signals = 0  # \uc0\u1048 \u1085 \u1080 \u1094 \u1080 \u1072 \u1083 \u1080 \u1079 \u1072 \u1094 \u1080 \u1103  \u1076 \u1083 \u1103  \u1076 \u1086 \u1089 \u1090 \u1091 \u1087 \u1072  \u1074  \u1101 \u1090 \u1086 \u1084  \u1089 \u1082 \u1086 \u1091 \u1087 \u1077 \
    if signal_text == TEXTS[context.user_data['language']]['signal_buy']:\
        buy_signals, sell_signals = get_signal_counts_for_arrows(\
            coin_id, interval, context=context)  # \uc0\u1055 \u1077 \u1088 \u1077 \u1076 \u1072 \u1077 \u1084  context\
        if buy_signals - sell_signals >= 3:  # \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1072 \u1080 \u1074 \u1072 \u1077 \u1084 \u1099 \u1081  \u1087 \u1086 \u1088 \u1086 \u1075  \u1076 \u1083 \u1103  "\u1089 \u1080 \u1083 \u1100 \u1085 \u1086 \u1075 \u1086 " \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1072 \
            # 3 \uc0\u1089 \u1090 \u1088 \u1077 \u1083 \u1082 \u1080  \u1074 \u1074 \u1077 \u1088 \u1093  \u1076 \u1083 \u1103  \u1089 \u1080 \u1083 \u1100 \u1085 \u1086 \u1075 \u1086  BUY (\u1079 \u1072 \u1084 \u1077 \u1085 \u1072  \u1082 \u1088 \u1091 \u1078 \u1082 \u1086 \u1074 )\
            signal_strength_arrows = "\uc0\u11014 \u65039 \u11014 \u65039 \u11014 \u65039  "\
    elif signal_text == TEXTS[context.user_data['language']]['signal_sell']:\
        buy_signals, sell_signals = get_signal_counts_for_arrows(\
            coin_id, interval, context=context)  # \uc0\u1055 \u1077 \u1088 \u1077 \u1076 \u1072 \u1077 \u1084  context\
        if sell_signals - buy_signals >= 3:  # \uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1072 \u1080 \u1074 \u1072 \u1077 \u1084 \u1099 \u1081  \u1087 \u1086 \u1088 \u1086 \u1075  \u1076 \u1083 \u1103  "\u1089 \u1080 \u1083 \u1100 \u1085 \u1086 \u1075 \u1086 " \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1072 \
            # 3 \uc0\u1089 \u1090 \u1088 \u1077 \u1083 \u1082 \u1080  \u1074 \u1085 \u1080 \u1079  \u1076 \u1083 \u1103  \u1089 \u1080 \u1083 \u1100 \u1085 \u1086 \u1075 \u1086  SELL (\u1079 \u1072 \u1084 \u1077 \u1085 \u1072  \u1082 \u1088 \u1091 \u1078 \u1082 \u1086 \u1074 )\
            signal_strength_arrows = "\uc0\u11015 \u65039 \u11015 \u65039 \u11015 \u65039  "\
    # ===  \uc0\u1050 \u1054 \u1053 \u1045 \u1062  \u1041 \u1051 \u1054 \u1050 \u1040  \u1057 \u1058 \u1056 \u1045 \u1051 \u1054 \u1050  ===\
\
    # \uc0\u1042 \u1089 \u1090 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1085 \u1077 \u1073 \u1086 \u1083 \u1100 \u1096 \u1086 \u1077  \u1089 \u1083 \u1091 \u1095 \u1072 \u1081 \u1085 \u1086 \u1077  \u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1080 \u1077  \u1074  price \u1080  interval_change_percent \u1087 \u1077 \u1088 \u1077 \u1076  \u1092 \u1086 \u1088 \u1084 \u1072 \u1090 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1080 \u1077 \u1084 \
    noisy_price = price + numpy.random.rand() * 1e-9  # \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1096 \u1091 \u1084  \u1082  \u1094 \u1077 \u1085 \u1077 \
    noisy_interval_change_percent = interval_change_percent + numpy.random.rand() * \\\
        1e-9\
\
    message = (TEXTS[context.user_data['language']]['price_coin'].format(coin_id, noisy_price) +  # \uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1084  noisy_price \u1079 \u1076 \u1077 \u1089 \u1100 \
               #  TEXTS[context.user_data['language']]['timeframe_change'].format(get_interval_label(interval, context.user_data['language']), noisy_interval_change_percent) + # \uc0\u1048 \u1089 \u1087 \u1086 \u1083 \u1100 \u1079 \u1091 \u1077 \u1084  noisy_interval_change_percent \u1079 \u1076 \u1077 \u1089 \u1100  \u1080  \u1103 \u1079 \u1099 \u1082  \u1080 \u1079  user_data\
               # \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1089 \u1090 \u1088 \u1077 \u1083 \u1082 \u1080  \u1087 \u1077 \u1088 \u1077 \u1076  \u1090 \u1077 \u1082 \u1089 \u1090 \u1086 \u1084  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1072 \
               TEXTS[context.user_data['language']]['signal_timeframe'].format(interval, signal_strength_arrows + signal_text) +\
               TEXTS[context.user_data['language']\
                     ]['trend_timeframe'].format(interval, trend_text)\
               )\
\
    # \uc0\u1041 \u1083 \u1086 \u1082  \u1089  \u1091 \u1088 \u1086 \u1074 \u1085 \u1103 \u1084 \u1080  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  \u1059 \u1044 \u1040 \u1051 \u1045 \u1053 \
\
    keyboard = [\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['button_1h'], callback_data=f"\{coin_id\}_1h"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['button_4h'], callback_data=f"\{coin_id\}_4h"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['button_12h'], callback_data=f"\{coin_id\}_12h"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['back_button'], callback_data=f"\{coin_id\}_back"),\
        ]\
    ]\
    reply_markup = InlineKeyboardMarkup(keyboard)\
\
    await query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)\
\
\
# \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085 \u1086  context\
def get_signal_counts_for_arrows(coin_id, interval='1d', context=None):\
    """\
    \uc0\u1042 \u1089 \u1087 \u1086 \u1084 \u1086 \u1075 \u1072 \u1090 \u1077 \u1083 \u1100 \u1085 \u1072 \u1103  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103  \u1076 \u1083 \u1103  \u1087 \u1086 \u1083 \u1091 \u1095 \u1077 \u1085 \u1080 \u1103  \u1082 \u1086 \u1083 \u1080 \u1095 \u1077 \u1089 \u1090 \u1074 \u1072  buy_signals \u1080  sell_signals\
    \uc0\u1076 \u1083 \u1103  \u1086 \u1087 \u1088 \u1077 \u1076 \u1077 \u1083 \u1077 \u1085 \u1080 \u1103  \u1089 \u1080 \u1083 \u1099  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1072  \u1080  \u1086 \u1090 \u1086 \u1073 \u1088 \u1072 \u1078 \u1077 \u1085 \u1080 \u1103  \u1089 \u1090 \u1088 \u1077 \u1083 \u1086 \u1082 .\
    """\
    hist_data = get_historical_data(coin_id, interval)\
    if not hist_data or len(hist_data) < 50:\
        return 0, 0  # \uc0\u1042 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1077 \u1084  0, \u1077 \u1089 \u1083 \u1080  \u1076 \u1072 \u1085 \u1085 \u1099 \u1077  \u1085 \u1077 \u1076 \u1086 \u1089 \u1090 \u1091 \u1087 \u1085 \u1099 \
\
    high = [h for h, _, _, _ in hist_data]\
    low = [l for _, l, _, _ in hist_data]\
    close = [c for _, _, c, _ in hist_data]\
    volume = [v for _, _, _, v in hist_data]\
    prices = close\
\
    indicators = calculate_indicators(prices, high, low, close, volume)\
    support, resistance = calculate_support_resistance(prices)\
\
    # === \uc0\u1056 \u1072 \u1089 \u1095 \u1077 \u1090  \u1091 \u1088 \u1086 \u1074 \u1085 \u1077 \u1081  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  ===\
    period_for_fibonacci_swing = 30\
    swing_high_fib = np.max(high[-period_for_fibonacci_swing:]\
                            ) if len(high) >= period_for_fibonacci_swing else None\
    swing_low_fib = np.min(low[-period_for_fibonacci_swing:]\
                           ) if len(low) >= period_for_fibonacci_swing else None\
    fibonacci_levels = \{\}\
    if swing_high_fib and swing_low_fib:\
        fibonacci_levels = calculate_fibonacci_levels(\
            swing_low_fib, swing_high_fib)\
    # === \uc0\u1050 \u1086 \u1085 \u1077 \u1094  \u1088 \u1072 \u1089 \u1095 \u1077 \u1090 \u1072  \u1091 \u1088 \u1086 \u1074 \u1085 \u1077 \u1081  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  ===\
\
    buy_signals = sell_signals = 0\
\
    # --- \uc0\u1057 \u1091 \u1097 \u1077 \u1089 \u1090 \u1074 \u1091 \u1102 \u1097 \u1080 \u1077  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1099  (\u1089  \u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1085 \u1099 \u1084 \u1080  \u1087 \u1086 \u1088 \u1086 \u1075 \u1072 \u1084 \u1080  RSI/Stochastic) ---\
    if close[-1] <= indicators['lower_bb']:\
        buy_signals += 1\
    elif close[-1] >= indicators['upper_bb']:\
        sell_signals += 1\
    if indicators['stoch_k'] < 25:  # Stochastic K \uc0\u1087 \u1077 \u1088 \u1077 \u1087 \u1088 \u1086 \u1076 \u1072 \u1085  (\u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  25)\
        buy_signals += 1\
    # Stochastic K \uc0\u1087 \u1077 \u1088 \u1077 \u1082 \u1091 \u1087 \u1083 \u1077 \u1085  (\u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  75)\
    elif indicators['stoch_k'] > 75:\
        sell_signals += 1\
    if indicators['sma_20'] > indicators['sma_50']:\
        buy_signals += 1\
    elif indicators['sma_20'] < indicators['sma_50']:\
        sell_signals += 1\
    if indicators['volume'] > np.mean(volume[-5:]) * 1.5:\
        if close[-1] > close[-2]:\
            buy_signals += 1\
        else:\
            sell_signals += 1\
    # \uc0\u1048 \u1089 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085 \u1086  \u1091 \u1089 \u1083 \u1086 \u1074 \u1080 \u1077  \u1076 \u1083 \u1103  SAR (\u1088 \u1072 \u1085 \u1077 \u1077  \u1073 \u1099 \u1083 \u1072  \u1086 \u1087 \u1077 \u1095 \u1072 \u1090 \u1082 \u1072 )\
    if indicators['sar'] > close[-1]:\
        buy_signals += 1  # \uc0\u1057 \u1080 \u1075 \u1085 \u1072 \u1083  BUY, \u1077 \u1089 \u1083 \u1080  SAR \u1085 \u1080 \u1078 \u1077  \u1094 \u1077 \u1085 \u1099 \
    else:\
        sell_signals += 1  # \uc0\u1057 \u1080 \u1075 \u1085 \u1072 \u1083  SELL, \u1077 \u1089 \u1083 \u1080  SAR \u1074 \u1099 \u1096 \u1077  \u1094 \u1077 \u1085 \u1099 \
    if support and resistance:\
        if close[-1] <= support * 1.005:\
            buy_signals += 1\
        elif close[-1] >= resistance * 0.995:\
            sell_signals += 1\
    if indicators['rsi'] > 65:  # RSI \uc0\u1087 \u1077 \u1088 \u1077 \u1082 \u1091 \u1087 \u1083 \u1077 \u1085  (\u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  65)\
        sell_signals += 1\
    elif indicators['rsi'] < 35:  # RSI \uc0\u1087 \u1077 \u1088 \u1077 \u1087 \u1088 \u1086 \u1076 \u1072 \u1085  (\u1080 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  35)\
        buy_signals += 1\
    if indicators['macd'] > indicators['signal']:\
        buy_signals += 1\
    elif indicators['macd'] < indicators['signal']:\
        sell_signals += 1\
    if indicators['ema_30'] > indicators['ema_100']:  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  ema_30 \u1080  ema_100\
        buy_signals += 1\
    elif indicators['ema_30'] < indicators['ema_100']:  # \uc0\u1048 \u1079 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  ema_30 \u1080  ema_100\
        sell_signals += 1\
    if indicators['willr'] < -80:\
        buy_signals += 1\
    elif indicators['willr'] > -20:\
        sell_signals += 1\
\
    # --- \uc0\u1057 \u1080 \u1075 \u1085 \u1072 \u1083 \u1099  \u1085 \u1072  \u1086 \u1089 \u1085 \u1086 \u1074 \u1077  OBV ---\
    obv = indicators['obv']\
    previous_obv = indicators.get('obv_previous')\
\
    if previous_obv is not None:\
        if obv > previous_obv:\
            buy_signals += 1\
        elif obv < previous_obv:\
            sell_signals += 1\
    # --- \uc0\u1050 \u1054 \u1053 \u1045 \u1062  \u1041 \u1051 \u1054 \u1050 \u1040  \u1044 \u1051 \u1071  OBV\
\
    # --- \uc0\u1053 \u1086 \u1074 \u1099 \u1077  \u1089 \u1080 \u1075 \u1085 \u1072 \u1083 \u1099  ---\
    # ADX\
    adx = calculate_adx(high, low, close)\
    if adx and adx > 25:\
        buy_signals += 1\
\
    # Ichimoku\
    conversion_line, base_line, leading_span_b = calculate_ichimoku(\
        high, low, close)\
    if conversion_line and base_line and leading_span_b:\
        if close[-1] > conversion_line and close[-1] > base_line:\
            buy_signals += 1\
        elif close[-1] < conversion_line and close[-1] < base_line:\
            sell_signals += 1\
\
    # --- \uc0\u1057 \u1080 \u1075 \u1085 \u1072 \u1083 \u1099  \u1085 \u1072  \u1086 \u1089 \u1085 \u1086 \u1074 \u1077  \u1091 \u1088 \u1086 \u1074 \u1085 \u1077 \u1081  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  ---\
    # (\uc0\u1057 \u1080 \u1075 \u1085 \u1072 \u1083 \u1099  \u1085 \u1072  \u1086 \u1089 \u1085 \u1086 \u1074 \u1077  \u1060 \u1080 \u1073 \u1086 \u1085 \u1072 \u1095 \u1095 \u1080  \u1091 \u1078 \u1077  \u1076 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085 \u1099  \u1074  get_trading_signal)\
\
    return buy_signals, sell_signals\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  7: \u1042 \u1089 \u1087 \u1086 \u1084 \u1086 \u1075 \u1072 \u1090 \u1077 \u1083 \u1100 \u1085 \u1099 \u1077  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1080 \
# ======================================================================\
\
# lang='ru' \uc0\u1073 \u1086 \u1083 \u1100 \u1096 \u1077  \u1085 \u1077  \u1085 \u1091 \u1078 \u1077 \u1085 , \u1085 \u1086  \u1086 \u1089 \u1090 \u1072 \u1074 \u1080 \u1084  \u1076 \u1083 \u1103  \u1089 \u1086 \u1074 \u1084 \u1077 \u1089 \u1090 \u1080 \u1084 \u1086 \u1089 \u1090 \u1080  \u1080  \u1077 \u1089 \u1083 \u1080  \u1079 \u1072 \u1093 \u1086 \u1090 \u1080 \u1084  \u1075 \u1083 \u1086 \u1073 \u1072 \u1083 \u1100 \u1085 \u1099 \u1081  \u1103 \u1079 \u1099 \u1082  \u1087 \u1086  \u1091 \u1084 \u1086 \u1083 \u1095 \u1072 \u1085 \u1080 \u1102 \
def get_interval_label(interval, lang='ru'):\
    """\
    \uc0\u1042 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1077 \u1090  \u1083 \u1086 \u1082 \u1072 \u1083 \u1080 \u1079 \u1086 \u1074 \u1072 \u1085 \u1085 \u1086 \u1077  \u1085 \u1072 \u1079 \u1074 \u1072 \u1085 \u1080 \u1077  \u1080 \u1085 \u1090 \u1077 \u1088 \u1074 \u1072 \u1083 \u1072  \u1074 \u1088 \u1077 \u1084 \u1077 \u1085 \u1080 .\
    """\
    interval_labels = \{\
        'ru': \{\
            '1h': TEXTS['ru']['interval_1h'],\
            '4h': TEXTS['ru']['interval_4h'],\
            '8h': TEXTS['ru']['interval_8h'],\
            '12h': TEXTS['ru']['interval_12h'],\
            '24h': TEXTS['ru']['interval_24h'],\
            '1d': TEXTS['ru']['interval_1d'],\
            'Change': TEXTS['ru']['interval_change'],\
        \},\
        'en': \{\
            '1h': TEXTS['en']['interval_1h'],\
            '4h': TEXTS['en']['interval_4h'],\
            '8h': TEXTS['en']['interval_8h'],\
            '12h': TEXTS['en']['interval_12h'],\
            '24h': TEXTS['en']['interval_24h'],\
            '1d': TEXTS['en']['interval_1d'],\
            'Change': TEXTS['en']['interval_change'],\
        \}\
    \}\
    # lang \uc0\u1090 \u1077 \u1087 \u1077 \u1088 \u1100  context.user_data['language']\
    return interval_labels[lang].get(interval, TEXTS[lang]['interval_change'])\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  8: \u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082 \u1080  CallbackQuery \u1082 \u1085 \u1086 \u1087 \u1086 \u1082 \
#                       (Inline \uc0\u1082 \u1085 \u1086 \u1087 \u1082 \u1080 , \u1086 \u1090 \u1074 \u1077 \u1090 \u1099  \u1085 \u1072  \u1085 \u1072 \u1078 \u1072 \u1090 \u1080 \u1103 )\
# ======================================================================\
\
async def start(update: Update, context: CallbackContext, query=None):  # \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1087 \u1072 \u1088 \u1072 \u1084 \u1077 \u1090 \u1088  query\
    """\uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099  /start, \u1074 \u1099 \u1074 \u1086 \u1076  \u1089 \u1090 \u1072 \u1088 \u1090 \u1086 \u1074 \u1086 \u1075 \u1086  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1103  \u1080  \u1082 \u1085 \u1086 \u1087 \u1086 \u1082 ."""\
    user_id = update.message.from_user.id if update.message else query.from_user.id  # \uc0\u1054 \u1087 \u1088 \u1077 \u1076 \u1077 \u1083 \u1103 \u1077 \u1084  user_id \u1076 \u1083 \u1103  message \u1080  callback_query\
    user_language = get_user_language(user_id)\
    context.user_data['language'] = user_language\
\
    keyboard = [\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),\
        ],\
    ]\
    reply_markup = InlineKeyboardMarkup(keyboard)\
    message_text = TEXTS[context.user_data['language']\
                         ]['start_message']  # \uc0\u1055 \u1086 \u1083 \u1091 \u1095 \u1072 \u1077 \u1084  \u1090 \u1077 \u1082 \u1089 \u1090  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1103 \
\
    # \uc0\u1045 \u1089 \u1083 \u1080  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103  \u1074 \u1099 \u1079 \u1074 \u1072 \u1085 \u1072  \u1080 \u1079  CallbackQuery (\u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 , \u1087 \u1088 \u1080  \u1089 \u1084 \u1077 \u1085 \u1077  \u1103 \u1079 \u1099 \u1082 \u1072 )\
    if query:\
        await query.answer()  # \uc0\u1055 \u1086 \u1076 \u1090 \u1074 \u1077 \u1088 \u1078 \u1076 \u1072 \u1077 \u1084  CallbackQuery\
        await query.edit_message_text(  # \uc0\u1056 \u1077 \u1076 \u1072 \u1082 \u1090 \u1080 \u1088 \u1091 \u1077 \u1084  \u1089 \u1091 \u1097 \u1077 \u1089 \u1090 \u1074 \u1091 \u1102 \u1097 \u1077 \u1077  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077 \
            message_text,\
            reply_markup=reply_markup,\
            parse_mode="Markdown"\
        )\
    else:  # \uc0\u1045 \u1089 \u1083 \u1080  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103  \u1074 \u1099 \u1079 \u1074 \u1072 \u1085 \u1072  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1086 \u1081  /start (\u1085 \u1086 \u1074 \u1086 \u1077  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077 )\
        await update.message.reply_text(  # \uc0\u1054 \u1090 \u1087 \u1088 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1085 \u1086 \u1074 \u1086 \u1077  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077 \
            message_text,\
            reply_markup=reply_markup,\
            parse_mode="Markdown"\
        )\
\
\
async def help(update: Update, context: CallbackContext):\
    """\uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099  /help \u1080  \u1082 \u1085 \u1086 \u1087 \u1082 \u1080  '\u10067  \u1055 \u1086 \u1084 \u1086 \u1097 \u1100 ', \u1074 \u1099 \u1074 \u1086 \u1076  \u1089 \u1087 \u1088 \u1072 \u1074 \u1082 \u1080 ."""\
    query = update.callback_query\
    await query.answer()\
    message = (TEXTS[context.user_data['language']]['help_message_header'] +\
               TEXTS[context.user_data['language']]['help_message_calculation_header'] +\
               TEXTS[context.user_data['language']]['help_message_calculation_text'] +\
               TEXTS[context.user_data['language']]['help_message_calculation_examples_header'] +\
               TEXTS[context.user_data['language']]['help_message_calculation_examples_text'] +\
               TEXTS[context.user_data['language']]['help_message_technical_analysis_header'] +\
               TEXTS[context.user_data['language']]['help_message_technical_analysis_text'] +\
               TEXTS[context.user_data['language']]['help_message_technical_analysis_features_header'] +\
               TEXTS[context.user_data['language']]['help_message_technical_analysis_features_text'] +\
               TEXTS[context.user_data['language']]['help_message_other_functions_header'] +\
               TEXTS[context.user_data['language']]['help_message_other_functions_text'])\
\
    keyboard = [\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),\
        ],\
    ]\
    reply_markup = InlineKeyboardMarkup(keyboard)\
\
    await query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)\
\
\
async def handle_donat(update: Update, context: CallbackContext):\
    """\uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082  \u1082 \u1085 \u1086 \u1087 \u1082 \u1080  '\u55357 \u56496  Donat', \u1074 \u1099 \u1074 \u1086 \u1076  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1103  \u1089  \u1080 \u1085 \u1092 \u1086 \u1088 \u1084 \u1072 \u1094 \u1080 \u1077 \u1081  \u1076 \u1083 \u1103  \u1076 \u1086 \u1085 \u1072 \u1090 \u1072 ."""\
    message = TEXTS[context.user_data['language']]['donat_message']\
\
    # ===  \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1082 \u1083 \u1072 \u1074 \u1080 \u1072 \u1090 \u1091 \u1088 \u1091  \u1075 \u1083 \u1072 \u1074 \u1085 \u1086 \u1075 \u1086  \u1084 \u1077 \u1085 \u1102  ===\
    keyboard = [\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),\
        ],\
        [\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),\
            InlineKeyboardButton(\
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),\
        ],\
    ]\
    reply_markup = InlineKeyboardMarkup(keyboard)\
    # ===  \uc0\u1050 \u1083 \u1072 \u1074 \u1080 \u1072 \u1090 \u1091 \u1088 \u1072  \u1075 \u1083 \u1072 \u1074 \u1085 \u1086 \u1075 \u1086  \u1084 \u1077 \u1085 \u1102  \u1076 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085 \u1072  ===\
\
    # \uc0\u1047 \u1072 \u1084 \u1077 \u1085 \u1077 \u1085 \u1086  \u1085 \u1072  edit_message_text \u1080  \u1076 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085  reply_markup\
    await update.callback_query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)\
\
\
async def button(update: Update, context: CallbackContext):\
    """\
    \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082  \u1074 \u1089 \u1077 \u1093  \u1082 \u1085 \u1086 \u1087 \u1086 \u1082  InlineKeyboard.\
    """\
    query = update.callback_query\
    user_id = query.from_user.id\
\
    if query.data == "CLOSE_HELP":\
        await close_help(update, context)\
    elif query.data == "TOP10_RISE":\
        await handle_top10_rise(update, context)\
    elif query.data == "TOP10_FALL":\
        await handle_top10_fall(update, context)\
    elif query.data == "HELP":\
        await help(update, context)\
    elif query.data == "DONAT":\
        await handle_donat(update, context)\
    # \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1072  \u1082 \u1085 \u1086 \u1087 \u1082 \u1080  English (\u1085 \u1072  \u1075 \u1083 \u1072 \u1074 \u1085 \u1086 \u1084  \u1101 \u1082 \u1088 \u1072 \u1085 \u1077 )\
    elif query.data == "LANGUAGE_EN":\
        set_user_language(user_id, 'en')\
        context.user_data['language'] = 'en'\
        # \uc0\u1042 \u1099 \u1079 \u1099 \u1074 \u1072 \u1077 \u1084  start \u1089  query \u1076 \u1083 \u1103  \u1088 \u1077 \u1076 \u1072 \u1082 \u1090 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1080 \u1103  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1103 !\
        await start(update, context, query=query)\
        await query.answer(text="Bot language switched to English!")\
    # \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1072  \u1082 \u1085 \u1086 \u1087 \u1082 \u1080  \u1056 \u1091 \u1089 \u1089 \u1082 \u1080 \u1081  (\u1085 \u1072  \u1075 \u1083 \u1072 \u1074 \u1085 \u1086 \u1084  \u1101 \u1082 \u1088 \u1072 \u1085 \u1077 )\
    elif query.data == "LANGUAGE_RU":\
        set_user_language(user_id, 'ru')\
        context.user_data['language'] = 'ru'\
        # \uc0\u1042 \u1099 \u1079 \u1099 \u1074 \u1072 \u1077 \u1084  start \u1089  query \u1076 \u1083 \u1103  \u1088 \u1077 \u1076 \u1072 \u1082 \u1090 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1080 \u1103  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1103 !\
        await start(update, context, query=query)\
        await query.answer(text="\uc0\u1071 \u1079 \u1099 \u1082  \u1073 \u1086 \u1090 \u1072  \u1087 \u1077 \u1088 \u1077 \u1082 \u1083 \u1102 \u1095 \u1077 \u1085  \u1085 \u1072  \u1088 \u1091 \u1089 \u1089 \u1082 \u1080 \u1081 !")\
    elif "_" in query.data and query.data != "CLOSE_HELP":\
        await handle_timeframe_data(update, context)\
\
\
async def close_help(update: Update, context: CallbackContext):\
    """\uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082  \u1076 \u1083 \u1103  \u1082 \u1085 \u1086 \u1087 \u1082 \u1080  "\u1047 \u1072 \u1082 \u1088 \u1099 \u1090 \u1100 " \u1074  \u1089 \u1087 \u1088 \u1072 \u1074 \u1082 \u1077 , \u1091 \u1076 \u1072 \u1083 \u1103 \u1077 \u1090  \u1082 \u1083 \u1072 \u1074 \u1080 \u1072 \u1090 \u1091 \u1088 \u1091 ."""\
    query = update.callback_query\
    await query.answer()\
    if query.message:\
        await query.edit_message_reply_markup(reply_markup=None)\
\
\
# ======================================================================\
#                       \uc0\u1057 \u1077 \u1082 \u1094 \u1080 \u1103  9: \u1043 \u1083 \u1072 \u1074 \u1085 \u1072 \u1103  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103  \u1079 \u1072 \u1087 \u1091 \u1089 \u1082 \u1072  \u1073 \u1086 \u1090 \u1072 \
# ======================================================================\
\
def main():\
    """\uc0\u1043 \u1083 \u1072 \u1074 \u1085 \u1072 \u1103  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103  \u1076 \u1083 \u1103  \u1079 \u1072 \u1087 \u1091 \u1089 \u1082 \u1072  \u1073 \u1086 \u1090 \u1072 ."""\
    application = Application.builder().token(\
        # \uc0\u1047 \u1072 \u1084 \u1077 \u1085 \u1080 \u1090 \u1077  \u1085 \u1072  \u1089 \u1074 \u1086 \u1081  \u1090 \u1086 \u1082 \u1077 \u1085  \u1073 \u1086 \u1090 \u1072 \
        "7568689765:AAHLeergcWCz3EyzMQ5GGqBCylFiQs2xn-Q").build()\
\
    application.add_handler(CommandHandler("start", start))\
    application.add_handler(MessageHandler(\
        filters.TEXT & ~filters.COMMAND, handle_text))\
    application.add_handler(CallbackQueryHandler(button))\
\
    application.run_polling(allowed_updates=Update.ALL_TYPES)\
\
\
if __name__ == "__main__":\
    main()\
\
\
if __name__ == "__main__":\
    main()\
}