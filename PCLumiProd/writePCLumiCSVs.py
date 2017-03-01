import ROOT
import sys
import argparse
import subprocess

parser=argparse.ArgumentParser()
parser.add_argument("-d",  "--dir", default="", help="EOS path to data cert tree files /store/user/..")
parser.add_argument("-f",  "--file",default="", help="EOS path to data cert tree file /store/user/..")
parser.add_argument("-l",  "--label",default="", help="For output files")
parser.add_argument("-r",  "--runs",default="", help="Comma separated list of runs.")
parser.add_argument("--nbxfile",default="NBX.csv", help="CSV file with run and NBX.")
parser.add_argument("--corrfile",default="", help="Corection file.")
parser.add_argument("--corrtfile",default="", help="Corection file of histograms.")
parser.add_argument("--yaml",default="", help="yaml file to append.")
parser.add_argument("--xing",default=1, help="Write per bx files.  Default 1.")
parser.add_argument("--justyaml",default=0, help="Only write yaml")
parser.add_argument("--xsec",default=9.05e6, type=float, help="PC cross section (default:  9.05e6 ub).")
args=parser.parse_args()

#Fill   Bfield    Runs 
fillInfo={}



fillInfo["5506"]=["3.800",[285143,285144,285146,285147]]
fillInfo["5505"]=["3.800",[285090,285091]]
fillInfo["5456"]=["3.800",[284077,284078]]
fillInfo["5451"]=["3.800",[284025,284029,284035,284036,284037,284038,284039,284040,284041,284042,284043,284044]]
fillInfo["5450"]=["3.800",[284006,284014]]
fillInfo["5448"]=["3.800",[283946,283964]]
fillInfo["5446"]=["3.800",[283933,283934]]
fillInfo["5443"]=["3.800",[283884,283885]]
fillInfo["5442"]=["3.800",[283876,283877,283878]]
fillInfo["5441"]=["3.800",[283863,283865]]
fillInfo["5439"]=["3.800",[283820,283830,283834,283835]]
fillInfo["5437"]=["3.800",[283672,283675,283676,283680,283681,283682,283685]]
fillInfo["5433"]=["3.800",[283548,283549,283550,283551,283553,283560]]
fillInfo["5427"]=["3.800",[283478,283481]]
fillInfo["5426"]=["3.800",[283469]]
fillInfo["5424"]=["3.800",[283453]]
fillInfo["5423"]=["3.800",[283407,283408,283413,283414,283415,283416]]
fillInfo["5422"]=["3.800",[283387]]
fillInfo["5421"]=["3.800",[283353,283358,283359]]
fillInfo["5418"]=["3.800",[283305,283306,283307,283308]]
fillInfo["5416"]=["3.800",[283270,283283]]
fillInfo["5412"]=["3.800",[283171]]
fillInfo["5406"]=["3.800",[283049,283050,283052,283059,283067]]
fillInfo["5405"]=["3.800",[283040,283041,283042,283043]]
fillInfo["5401"]=["3.800",[282917,282918,282919,282920,282921,282922,282923,282924]]
fillInfo["5395"]=["3.800",[282842]]
fillInfo["5394"]=["3.800",[282799,282800,282807,282814]]
fillInfo["5393"]=["3.800",[282730,282731,282732,282733,282734,282735]]
fillInfo["5391"]=["3.800",[282707,282708,282709,282710,282711,282712]]
fillInfo["5386"]=["3.800",[282663]]
fillInfo["5385"]=["3.800",[282649,282650]]
fillInfo["5370"]=["3.800",[282408]]
fillInfo["5355"]=["3.800",[282092]]
fillInfo["5352"]=["3.800",[282033,282034,282035,282037]]
fillInfo["5351"]=["3.800",[281974,281975,281976]]
fillInfo["5345"]=["3.800",[281797]]
fillInfo["5340"]=["3.800",[281707,281726,281727]]
fillInfo["5339"]=["3.800",[281663,281671,281674,281680,281685,281686,281689,281691,281693]]
fillInfo["5338"]=["3.800",[281638,281639,281640,281641]]
fillInfo["5332"]=["3.800",[281616]]
fillInfo["5331"]=["3.800",[281613]]
fillInfo["5330"]=["3.800",[281601,281602,281603,281604]]
fillInfo["5288"]=["3.800",[280383,280384,280385]]
fillInfo["5287"]=["3.800",[280327,280330,280349,280361,280363,280364]]
fillInfo["5282"]=["3.800",[280238,280239,280240,280241,280242,280249,280251]]
fillInfo["5279"]=["3.800",[280187,280188,280189,280190,280191,280192,280194]]
fillInfo["5277"]=["3.800",[279993,279994,279995,280001,280002,280006,280007,280013,280014,280015,280016,280017,280018,280019,280020,280021,280022,280023,280024]]
fillInfo["5276"]=["3.800",[279975]]
fillInfo["5275"]=["3.800",[279966]]
fillInfo["5274"]=["3.800",[279931]]
fillInfo["5270"]=["3.796",[279887]]
fillInfo["5267"]=["2.437",[279844,279845,279846,279848,279849,279850,279851,279852,279853,279854,279855,279856,279857,279858,279859,279860,279861,279862,279864,279865]]
fillInfo["5266"]=["3.799",[279841]]
fillInfo["5265"]=["3.799",[279823]]
fillInfo["5264"]=["3.799",[279794]]
fillInfo["5261"]=["3.799",[279760,279766,279767]]
fillInfo["5258"]=["3.799",[279715,279716]]
fillInfo["5257"]=["3.799",[279691,279694]]
fillInfo["5256"]=["3.799",[279681,279682,279683,279684,279685]]
fillInfo["5254"]=["3.799",[279667]]
fillInfo["5253"]=["3.799",[279653,279654,279656,279657,279658]]
fillInfo["5251"]=["3.799",[279588]]

fillInfo["5247"]=["3.799",[279479,279480,279484,279487,279488,279489]]
fillInfo["5246"]=["3.799",[279473]]
fillInfo["5229"]=["3.799",[279115,279116]]
fillInfo["5223"]=["3.799",[279080]]
fillInfo["5222"]=["3.799",[279071,279072,279073]]
fillInfo["5219"]=["3.799",[279024,279028,279029]]
fillInfo["5213"]=["3.799",[278986]]
fillInfo["5211"]=["3.799",[278969,278975,278976]]
fillInfo["5210"]=["3.799",[278962,278963]]
fillInfo["5209"]=["3.799",[278957]]
fillInfo["5206"]=["3.799",[278923]]
fillInfo["5205"]=["3.799",[278873,278874,278875]]
fillInfo["5199"]=["3.799",[278820,278821,278822]]
fillInfo["5198"]=["3.799",[278801,278802,278803,278804,278805,278806,278807,278808]]
fillInfo["5197"]=["3.799",[278769,278770]]
fillInfo["5196"]=["3.799",[278765]]
fillInfo["5194"]=["3.799",[278761]]
fillInfo["5187"]=["3.799",[278509]]
fillInfo["5183"]=["3.799",[278406]]
fillInfo["5181"]=["3.799",[278345,278346,278349,278366]]
fillInfo["5179"]=["3.799",[278315]]
fillInfo["5173"]=["3.799",[278308,278309,278310]]
fillInfo["5170"]=["3.799",[278288,278289,278290]]
fillInfo["5169"]=["3.799",[278273,278274]]
fillInfo["5163"]=["3.799",[278239,278240]]
fillInfo["5162"]=["3.799",[278193]]
fillInfo["5161"]=["3.799",[278167,278175]]
fillInfo["5154"]=["3.799",[278017,278018]]
fillInfo["5151"]=["3.799",[277981,277982,277983,277984,277985,277990,277991,277992]]
fillInfo["5149"]=["3.799",[277932,277933,277934,277935]]
fillInfo["5117"]=["3.799",[277420]]
fillInfo["5116"]=["3.799",[277305]]
fillInfo["5112"]=["3.799",[277217,277218,277219,277220]]
fillInfo["5111"]=["3.799",[277194,277202]]
fillInfo["5110"]=["3.799",[277180]]
fillInfo["5109"]=["3.799",[277166,277168]]
fillInfo["5108"]=["3.799",[277148]]
fillInfo["5107"]=["3.799",[277126,277127]]

fillInfo["5106"]=["3.799",[277093,277094,277096]]
fillInfo["5105"]=["3.799",[277069,277070,277071,277072,277073,277075,277076,277081,277086,277087]]
fillInfo["5102"]=["3.799",[276940,276941,276942,276944,276945,276946,276947,276948,276950]]
fillInfo["5101"]=["3.799",[276935]]
fillInfo["5097"]=["3.799",[276870]]
fillInfo["5096"]=["3.799",[276831,276832,276834,276835,276836,276837]]
fillInfo["5095"]=["3.799",[276807,276808,276810,276811]]
fillInfo["5093"]=["3.799",[276775,276776,276794]]
fillInfo["5091"]=["3.799",[276653,276655,276659]]
fillInfo["5085"]=["3.799",[276581,276582,276583,276584,276585,276586,276587]]
fillInfo["5083"]=["3.799",[276542,276543,276544,276545]]
fillInfo["5080"]=["3.799",[276525,276527,276528]]
fillInfo["5078"]=["3.799",[276495,276501,276502]]
fillInfo["5076"]=["3.799",[276437,276453,276454,276455,276456,276457,276458]]
fillInfo["5073"]=["3.799",[276352,276355,276357,276361,276363,276384]]
fillInfo["5072"]=["3.799",[276315,276317,276318,276326,276327]]
fillInfo["5071"]=["3.799",[276282,276283]]
fillInfo["5069"]=["2.294",[276225,276226,276229,276232,276235,276237,276242,276243,276244]]
fillInfo["5068"]=["0.019",[276215,276216,276217]]
fillInfo["5060"]=["3.800",[276092,276093,276095,276097]]
fillInfo["5059"]=["3.048",[276054,276062,276063,276064,276071,276072]]
fillInfo["5056"]=["3.800",[275963]]
fillInfo["5052"]=["3.800",[275911,275912,275913,275918,275920,275921,275922,275923,275931]]
fillInfo["5048"]=["3.800",[275886,275887,275890]]
fillInfo["5045"]=["3.800",[275828,275829,275831,275832,275833,275834,275835,275836,275837,275838,275841,275846,275847]]
fillInfo["5043"]=["3.800",[275757,275758,275759,275761,275763,275764,275766,275767,275768,275769,275772,275773,275774,275776,275777,275778,275781,275782,275783]]
fillInfo["5038"]=["3.801",[275656,275657,275658,275659]]
fillInfo["5030"]=["3.801",[275375,275376]]
fillInfo["5029"]=["3.801",[275370,275371]]
fillInfo["5028"]=["3.801",[275344,275345]]
fillInfo["5027"]=["3.801",[275319,275326,275337,275338]]
fillInfo["5026"]=["3.801",[275309,275310,275311]]
fillInfo["5024"]=["3.801",[275282,275283,275284,275285,275286,275289,275290,275291,275292,275293]]
fillInfo["5021"]=["3.801",[275124,275125]]
fillInfo["5020"]=["3.801",[275059,275062,275063,275064,275066,275067,275068,275073,275074]]
fillInfo["5017"]=["3.801",[274998,274999,275000,275001]]
fillInfo["5013"]=["3.801",[274966,274967,274968,274969,274970,274971]]
fillInfo["5005"]=["3.801",[274954,274955,274956,274957,274958,274959]]
fillInfo["4990"]=["3.801",[274440,274441,274442,274443]]
fillInfo["4988"]=["3.801",[274420,274421,274422]]
fillInfo["4985"]=["3.801",[274387,274388]]
fillInfo["4984"]=["3.801",[274382]]
fillInfo["4980"]=["3.801",[274335,274336,274337,274338,274339,274344,274345]]
fillInfo["4979"]=["3.801",[274314,274315,274316,274317,274318,274319]]
fillInfo["4976"]=["3.801",[274282,274283,274284,274285,274286]]
fillInfo["4965"]=["3.801",[274250,274251]]
fillInfo["4964"]=["3.801",[274240,274241,274243,274244]]
fillInfo["4961"]=["3.801",[274198,274199,274200]]
fillInfo["4960"]=["3.801",[274172]]
fillInfo["4958"]=["3.801",[274157,274159,274160,274161]]
fillInfo["4956"]=["3.801",[274142,274146]]
fillInfo["4954"]=["3.801",[274100,274102,274103,274104,274105,274106,274107,274108]]
fillInfo["4953"]=["3.801",[274094]]
fillInfo["4947"]=["3.801",[273725,273728,273730]]
fillInfo["4945"]=["3.801",[273588,273589,273590,273591,273592,273593]]
fillInfo["4942"]=["3.801",[273554,273555]]
fillInfo["4937"]=["3.801",[273522,273523,273526,273531,273537]]
fillInfo["4935"]=["3.801",[273502,273503,273504]]
fillInfo["4930"]=["3.800",[273492,273493,273494]]
fillInfo["4926"]=["3.799",[273445,273446,273447,273448,273449,273450]]
fillInfo["4925"]=["3.799",[273425,273426]]
fillInfo["4924"]=["3.799",[273402,273403,273404,273405,273406,273407,273408,273409,273410,273411,273412]]
fillInfo["4919"]=["3.799",[273290,273291,273292,273294,273295,273296,273299,273301,273302]]
fillInfo["4915"]=["3.799",[273150,273158]]
fillInfo["4910"]=["3.799",[273013,273017,273063]]
fillInfo["4906"]=["3.799",[272935,272936]]
fillInfo["4905"]=["3.799",[272922,272923,272924,272925,272926,272927,272930]]
fillInfo["4896"]=["3.799",[272827,272828]]
fillInfo["4895"]=["3.799",[272811,272812,272814,272815,272816,272818]]
fillInfo["4892"]=["3.799",[272798]]
fillInfo["4890"]=["3.799",[272782,272783,272784,272785,272786,272787]]
fillInfo["4889"]=["3.799",[272774,272775,272776]]
fillInfo["4888"]=["3.799",[72760,272761,272762]]
fillInfo["4879"]=["3.799",[272006,272007,272008,272010,272011,272012,272014,272016,272017,272018,272019,272021,272022]]
fillInfo["4874"]=["0.059",[271645,271646,271648,271649,271651,271652,271653,271654,271656,271658]]
fillInfo["4861"]=["0.019",[271304,271305,271306,271307,271310,271312,271313,271314,271317,271318,271319,271321,271322,271323,271324,271327,271328,271329,271330,271331,271332,271336,271337,271338,271342]]
fillInfo["4856"]=["0.019",[271184,271187,271188,271190,271191,271192,271193,271195,271196,271197,271213,271214,271215,271216,271217,271219,271220,271221,271228,271230,271231,271232,271234]]
fillInfo["4852"]=["0.019",[71076,271077,271080,271081,271082,271083,271084]]
fillInfo["4851"]=["0.019",[71036,271037,271044,271045,271046,271047,271048,271049,271050,271052,2710]]


fillInfo["4647"]=["3.798513298",[262325,262326,262327,262328]]
fillInfo["4643"]=["3.798513298",[262270,262271,262272,262273,262274,262275,262277]]
fillInfo["4640"]=["3.798513298",[262248,262249,262250,262252,262253,262254]]
fillInfo["4639"]=["3.798513298",[262235]]
fillInfo["4638"]=["3.798513298",[262204,262205]]
fillInfo["4634"]=["3.798513298",[262081,262114,262121,262137,262147,262156,262157,262163,262164,262165,262167,262168,262169,262170,262171,262172,262173,262174]]
fillInfo["4569"]=["3.798970769",[260627]]
fillInfo["4565"]=["3.798970769",[260593]]
fillInfo["4562"]=["3.798970769",[260575,260576,260577]]
fillInfo["4560"]=["1.544083541",[260488,260489,260490,260491,260492,260493,260496,260497,260498,260499,260510,260527,260528,260532,260533,260534,260536,260538,260540,260541]]
fillInfo["4557"]=["3.719991773",[260424,260425,260426,260427,260431,260433,260439]]
fillInfo["4555"]=["3.80020411",[260373]]
fillInfo["4545"]=["0.019018997",[260230,260232,260233,260234,260235]]
fillInfo["4540"]=["0.019018997",[260099,260100,260101,260102,260104,260105,260107,260108,260114,260119,260132,260135,260136]]
fillInfo["4538"]=["0.019018997",[260034,260035,260036,260037,260038,260039,260041,260043,260061,260062,260066]]
fillInfo["4536"]=["0.019018997",[259968,259971,259972,259973]]
fillInfo["4532"]=["3.800569273",[259884,259890,259891]]
fillInfo["4530"]=["3.800569273",[259861,259862]]
fillInfo["4528"]=["3.800569273",[259809,259810,259811,259812,259813,259817,259818,259820,259821,259822]]
fillInfo["4525"]=["3.800569273",[259721]]
fillInfo["4522"]=["3.800569273",[259681,259682,259683,259685,259686]]
fillInfo["4519"]=["3.800569273",[259636,259637]]
fillInfo["4518"]=["3.800569273",[259626]]
fillInfo["4513"]=["3.800569273",[259464]]
fillInfo["4511"]=["3.800569273",[259429,259431]]
fillInfo["4510"]=["3.800569273",[259399]]
fillInfo["4509"]=["3.800569273",[259384,259385,259388]]
fillInfo["4505"]=["3.800569273",[259351,259352,259353]]
fillInfo["4499"]=["3.800569273",[259236,259237]]
fillInfo["4496"]=["3.800569273",[259199,259200,259201,259202,259204,259205,259207,259208]]
fillInfo["4495"]=["3.800569273",[259152,259157,259158,259159,259161,259162,259163,259164,259167]]
fillInfo["4485"]=["3.800569273",[258741,258742,258745,258749,258750]]
fillInfo["4479"]=["3.800569273",[258702,258703,258705,258706,258712,258713,258714]]
fillInfo["4477"]=["3.800569273",[258694]]
fillInfo["4476"]=["3.800569273",[258655,258656]]
fillInfo["4467"]=["3.800569273",[258425,258426,258427,258428,258432,258434,258440,258442,258443,258444,258445,258446,258448]]
fillInfo["4466"]=["3.800569273",[258403]]
fillInfo["4464"]=["3.799768191",[258335]]
fillInfo["4463"]=["3.799768191",[258312,258313,258319,258320]]
fillInfo["4462"]=["3.799768191",[258287]]
fillInfo["4455"]=["3.799768191",[258211,258213,258214,258215]]
fillInfo["4452"]=["3.799768191",[258174,258175,258177]]
fillInfo["4449"]=["3.799768191",[258157,258158,258159]]
fillInfo["4448"]=["3.799768191",[258129,258136]]
fillInfo["4444"]=["3.799768191",[257968,257969]]
fillInfo["4440"]=["3.799768191",[257804,257805,257816,257818,257819,257821,257822,257823,257824,257825]]
fillInfo["4437"]=["3.799768191",[257750,257751]]
fillInfo["4435"]=["3.799768191",[257721,257722,257723,257725,257732,257733,257734,257735]]
fillInfo["4434"]=["3.799768191",[257682]]
fillInfo["4432"]=["3.799768191",[257645]]
fillInfo["4428"]=["3.799768191",[257613,257614]]
fillInfo["4426"]=["3.799768191",[257599]]
fillInfo["4423"]=["3.799768191",[257531]]
fillInfo["4420"]=["3.799768191",[257487,257490]]
fillInfo["4418"]=["3.799768191",[257461]]
fillInfo["4410"]=["3.799768191",[257394,257395,257396,257397,257398,257399,257400]]
fillInfo["4402"]=["1.68653331",[257027,257032,257035,257038,257042,257044,257055,257058,257059]]
fillInfo["4398"]=["3.799673444",[256936,256941]]
fillInfo["4397"]=["3.799673444",[256926]]
fillInfo["4393"]=["3.799673444",[256866,256867,256868,256869]]
fillInfo["4391"]=["3.799673444",[256842,256843]]
fillInfo["4386"]=["3.799673444",[256801]]
fillInfo["4384"]=["3.799673444",[256728,256729,256730,256733,256734]]
fillInfo["4381"]=["3.799673444",[256673,256674,256675,256676,256677]]
fillInfo["4376"]=["3.799673444",[256630]]
fillInfo["4364"]=["0.018967839",[256464]]
fillInfo["4363"]=["0.018967839",[256443,256444,256445,256446,256447,256448]]
fillInfo["4360"]=["0.018967839",[256423,256424]]
fillInfo["4356"]=["0.018967839",[256405,256406]]
fillInfo["4349"]=["0.018967839",[256347,256348,256349,256350,256353,256355]]
fillInfo["4342"]=["0.018967839",[256245]]
fillInfo["4341"]=["0.018967839",[256234,256235,256236,256237]]
fillInfo["4337"]=["0.018967839",[256214,256215,256216,256217]]
fillInfo["4332"]=["0.018967839",[256167,256168,256169,256171]]
fillInfo["4323"]=["0.018967839",[256001,256002,256003,256004]]
fillInfo["4322"]=["0.018967839",[255981,255982,255983,255984,255985,255986,255987,255988,255989,255990,255993]]
fillInfo["4269"]=["3.799233459",[255019,255029,255030,255031]]
fillInfo["4268"]=["3.799233459",[255003]]
fillInfo["4266"]=["3.799233459",[254980,254982,254983,254984,254985,254986,254987,254989,254991,254992,254993]]
fillInfo["4257"]=["3.799233459",[254914]]
fillInfo["4256"]=["3.799233459",[254905,254906,254907]]
fillInfo["4254"]=["3.799233459",[254879]]
fillInfo["4249"]=["3.799233459",[254852]]
fillInfo["4246"]=["3.799233459",[254833]]
fillInfo["4243"]=["3.799233459",[254790]]
fillInfo["4231"]=["0.019004049",[254608]]
fillInfo["4225"]=["0.019004049",[254532]]
fillInfo["4224"]=["0.019004049",[254512]]
fillInfo["4220"]=["0.019004049",[254437,254450,254451,254453,254454,254455,254456,254457,254458,254459]]
fillInfo["4219"]=["0.019004049",[254416]]
fillInfo["4214"]=["0.019004049",[254380]]
fillInfo["4212"]=["0.019004049",[254362,254364,254366,254367,254368]]
fillInfo["4211"]=["0.019004049",[254349]]
fillInfo["4210"]=["0.019004049",[254340,254341,254342]]
fillInfo["4208"]=["0.019004049",[254332]]
fillInfo["4207"]=["0.019004049",[254306,254307,254308,254309,254310,254313,254314,254315,254316,254317,254318,254319]]
fillInfo["4205"]=["1.151918971",[254280,254282,254283,254284,254285,254289,254290,254292,254293,254294]]
fillInfo["4201"]=["3.800328948",[254227,254229,254230,254231,254232]]
fillInfo["4020"]=["0.018957838",[252126]]
fillInfo["4019"]=["0.018957838",[252116]]
fillInfo["4008"]=["3.799702722",[251883]]
fillInfo["4006"]=["3.799702722",[251864]]
fillInfo["4001"]=["3.799702722",[251781]]
fillInfo["3996"]=["3.799702722",[251717,251718,251721]]
fillInfo["3992"]=["3.799702722",[251636,251638,251640,251642,251643]]
fillInfo["3988"]=["3.799702722",[251559,251560,251561,251562]]
fillInfo["3986"]=["3.799702722",[251548]]
fillInfo["3983"]=["3.799702722",[251521,251522,251523]]
fillInfo["3981"]=["2.849426279",[251491,251493,251496,251497,251498,251499,251500]]
fillInfo["3976"]=["3.799731187",[251244,251249,251250,251251,251252]]
fillInfo["3974"]=["3.799731187",[251131,251134,251142,251143,251147,251149,251150,251153,251155,251156,251160,251161,251162,251163,251164,251167,251168,251170]]
fillInfo["3971"]=["3.799731187",[251022,251023,251024,251025,251026,251027,251028]]
fillInfo["3965"]=["0.018936371",[250930,250931,250932]]
fillInfo["3962"]=["0.036359372",[250885,250886,250889,250890,250891,250892,250893,250895,250896,250897,250898,250899,250901,250902]]
fillInfo["3960"]=["0.018828806",[250862,250863,250864,250865,250866,250867,250868,250869,250871]]
fillInfo["3858"]=["0.018828806",[248025,248026,248027,248028,248029,248030,248031,248032,248033,248035,248036,248037,248038]]
fillInfo["3857"]=["0.018828806",[247981,247982,247983,247987,247989,247990,247991,247992,247994,247996,247998,248000,248002,248003,248004,248005,248006,248007,248009]]
fillInfo["3855"]=["0.018828806",[247910,247911,247912,247913,247914,247915,247917,247919,247920,247921,247923,247924,247926,247927,247928,247931,247933,247934]]
fillInfo["3851"]=["0.018828806",[247702,247703,247704,247705,247707,247708,247710,247711,247716,247718,247719,247720]]
fillInfo["3850"]=["0.018828806",[247685]]
fillInfo["3848"]=["0.018828806",[247642,247644,247646,247647,247648]]
fillInfo["3847"]=["0.018828806",[247623]]
fillInfo["3846"]=["0.018828806",[247607,247609,247610,247611,247612]]
fillInfo["3835"]=["0.018828806",[247377,247379,247380,247381,247382,247383,247384,247385,247386,247387,247388,247389,247394,247395,247397,247398]]
fillInfo["3833"]=["0.018828806",[247302,247303,247305,247306,247307,247309,247310,247313,247317,247318,247319,247320,247323,247324,247326,247328,247333,247334,247335,247336]]
fillInfo["3829"]=["0.018828806",[247231,247232,247233,247234,247235,247236,247237,247238,247240,247241,247243,247244,247245,247246,247247,247248,247250,247251,247252,247253,247255,247256,247259,247261,247262,247263,247265,247266,247267]]
fillInfo["3824"]=["0.018828806",[247068,247069,247070,247073,247076,247077,247078,247079,247081]]
fillInfo["3820"]=["0.018842477",[246951,246953,246954,246956,246957,246958,246959,246960,246961,246962,246963]]
fillInfo["3819"]=["0.0188423",[246908,246912,246913,246914,246919,246920,246923,246926,246930,246933,246934,246936]]

#fillLIST=["4201","4205","4207","4208","4210","4211","4212","4214","4219","4220","4224","4225","4231","4243","4246","4249","4254","4256","4257","4266","4268","4269","4322","4323","4332","4337","4341","4342","4349","4356","4360","4363","4364","4376","4381","4384","4386","4391","4393","4397","4398","4402","4410","4418","4420","4423","4426","4428","4432","4434","4435","4437","4440","4444","4448","4449","4452","4455","4462","4463","4464","4466","4467","4476","4477","4479","4485","4495","4496","4499","4505","4509","4510","4511","4513","4518","4519","4522","4525","4528","4530","4532","4536","4538","4540","4545","4555","4557","4851","4879","4888","4889","4895","4915","4926","4937","4942","4945","4947","4953","4954","4956","4958","4960","4964","4965","4979"]

##for FILL in fillLIST:
##    firstRun=fillInfo[FILL][1][0]
##    print FILL,",",firstRun
##sys.exit()

def findRunInFill(run):
    for fill in fillInfo:
        if int(run) in fillInfo[fill][1]:
            #print fill, run
            return fill

    print run,"not in list"
    return -1


NBXPerRun={}
NBXPerFill={}
nbxfile=open(args.nbxfile)
for line in nbxfile.readlines():
    items=line.split(",")
    try:
        #run=int(items[0])
        fill=int(items[0])
        NBX=int(items[1])
        NBXPerFill[fill]=NBX
    except:
        print "Problem with line",line

nbxfile.close()
#print NBXPerRun


corrPerRun={}
corrPerFill={}
if args.corrfile!="":
    corrfile=open(args.corrfile)
    for line in corrfile.readlines():
        items=line.split(",")
        try:
            #run=int(items[0])
            #LS1=int(items[1])
            #LSN=int(items[2])
            #corrFac=float(items[3])
            #if corrFac<0.85: 
            #    print run,corrFac,"not using"
            #    continue
            #if not corrPerRun.has_key(run):
            #    corrPerRun[run]={}
            #corrPerRun[run][(LS1,LSN)]=corrFac
            fill=int(items[0])
            corrFac=float(items[1])
            corrPerFill[fill]=corrFac
        except:
            print "Problem with line",line
    
    corrfile.close()
print corrPerFill

vetoCorrRuns=[]
availableCorrHists={}
if args.corrtfile!="":
    corrtfile=ROOT.TFile.Open(args.corrtfile)
    histKeys=corrtfile.GetListOfKeys()
    for histKey in histKeys:
        histName=histKey.GetName()
        # example hist name:  Ratio_Correction_275376_LS3101_LS3200
        if histName.find("Ratio_Correction_")!=-1:
            beforeName=histName.replace("Ratio_Correction","Before_Corr")
            h_before=corrtfile.Get(beforeName)
              
            nameParts=histName.split("_") 
            run=int(nameParts[2])
            thisFill=int(findRunInFill(run))
            if thisFill not in NBXPerFill.keys():
                print thisFill,"not in fills"
                continue
            nbx=NBXPerFill[thisFill]
            entries=h_before.GetEntries()
            if float(entries)/float(nbx)<7:
                continue
            if run in vetoCorrRuns:
                continue
            lsstart=int(nameParts[-2].split("LS")[1])
            lsend=int(nameParts[-1].split("LS")[1])
            if not availableCorrHists.has_key(run):
                availableCorrHists[run]=[]
            availableCorrHists[run].append([lsstart,lsend])

print availableCorrHists

f_LHC=11245.6

rawPCCFile=open("rawPCC"+args.label+".csv", 'a+')
PCLumiFile=open("PCLumi"+args.label+".csv", 'a+')
if args.xing==1:
    rawPCCFilePerBX=open("rawPCCPerBX"+args.label+".csv", 'a+')
    PCLumiFilePerBX=open("PCLumiPerBX"+args.label+".csv", 'a+')
if args.yaml!="":
    yamlFile=open(args.yaml, 'a+')


if args.yaml!="":
    if len(yamlFile.readlines())==0:
        yamlFile.write("name: pcc2016v1\n")
        yamlFile.write("applyto: lumi\n")
        yamlFile.write("datasource: pxl\n")
        yamlFile.write("istypedefault: 0\n")
        yamlFile.write("comments:  2016 data up to June 2nd\n")
        yamlFile.write("since:\n")

    fills=corrPerFill.keys()
    fills.sort()
    lastFill=0
    for thisFill in fills:
        run=fillInfo[str(thisFill)][1][0]
        yamlFile.write("      - "+str(run)+":\n")
        #yamlFile.write("              func: poly1dWafterglow\n")
        #yamlFile.write("              payload: {'coefs': '"+str(f_LHC/float(args.xsec))+",0.', 'afterglowthresholds':'(1,"+str(corrPerFill[thisFill])+")'}\n")
        yamlFile.write("              func: poly1d\n")
        yamlFile.write("              payload: {'coefs': '"+str(f_LHC/float(args.xsec))+",0.'}\n")
        yamlFile.write("              comments: 2016, egev 6500, PROTPHYS, Uncorrected VdM May 27th 2016\n")
    
    
    yamlFile.close()


if args.justyaml==1:
    sys.exit()

filenames=[]
if args.file!="":
    #filenames.append("root://eoscms//eos/cms"+args.file)
    filenames.append(args.file)
if args.dir!="":
    if args.dir.find("/store") ==0:
        filesInDirString=subprocess.check_output(["/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select","ls", args.dir])
    else:
        filesInDirString=subprocess.check_output(["ls", args.dir])
    for fileInDir in filesInDirString.split("\n"):
        if fileInDir.find(".root")!=-1:
            if args.dir.find("/store") ==0:
                filenames.append("root://eoscms//eos/cms"+args.dir+"/"+fileInDir)
            else:
                filenames.append(args.dir+"/"+fileInDir)
try:
    if args.runs!="":
        args.runs=args.runs.split(",")
except:
    args.runs=""

#if args.corrraw!=0:

runLSs=[]
for filename in filenames:
    try:
        tfile=ROOT.TFile.Open(filename)
        tree=tfile.Get("certtree")
       
        print "file opened",filename
        nEntries=tree.GetEntries()
        
        print "nEntries ",nEntries
        if args.corrtfile!="":
            thisCorrHist=0
            allCorrHist=0
            lastFill=0

        for iEnt in range(nEntries):
            tree.GetEntry(iEnt)
            if args.runs!="":
                if str(tree.run) not in args.runs:
                    continue

            if (tree.run,tree.LS) in runLSs:
                print "already found",tree.run,tree.LS,"skipping"
                continue
            else:
                runLSs.append((tree.run,tree.LS))

            thisFill=int(findRunInFill(tree.run))
            if thisFill not in NBXPerFill.keys():
                print thisFill,"not in fills"
                continue

            if args.corrtfile!="":
                #if thisCorrHist==0 or thisFill!=lastFill:
                try:
                    #find run in list of available 
                    histSuffix=""
                    thisCorrHist=0
                    allCorrHist=0
                    if tree.run in availableCorrHists.keys():
                        #find ls in range
                        bestLSRange=[-9999,-9999]
                        distFromLS=9999
                        exactFind=False
                        for lsrange in availableCorrHists[tree.run]:
                            #found it exactly
                            if tree.LS>=lsrange[0] and tree.LS<=lsrange[1]:
                                bestLSRange=lsrange
                                exactFind=True
                                break
                            #saving the closest
                            else:
                                thisDistFromLS=min(abs(tree.LS-bestLSRange[0]),abs(tree.LS-bestLSRange[1]))
                                if distFromLS>thisDistFromLS:
                                    bestLSRange=lsrange
                                    distFromLS=thisDistFromLS

                        if not exactFind:
                            print "Using",bestLSRange,"for",tree.LS

                        histSuffix=str(tree.run)+"_LS"+str(bestLSRange[0])+"_LS"+str(bestLSRange[1])
                        thisCorrHist=corrtfile.Get("Ratio_Correction_"+histSuffix)
                        allCorrHist=corrtfile.Get("Overall_Ratio_"+histSuffix)
                            
                    else:
                        # FIXME look for other runs in the same fill
                        print tree.run,"missing from runs with corrections"
                        runsInThisFill=fillInfo[thisFill][1]
                        closestRunWithCorr=0
                        distToClosestRun=1000000
                        for runInFill in runsInThisFill:
                            if runInFill in availableCorrHists.keys():
                               thisDist=abs(closestRunWithCorr-tree.run)
                               if thisDist<distToClosestRun:
                                  distToClosestRun=thisDist
                                  closestRunWithCorr=runInFill

                        #run earlier than this one... take lastest LS range
                        if tree.run>closestRunWithCorr:
                            bestLSRange=availableCorrHists[closestRunWithCorr][-1]
                        else:
                        #run later than this one... take earliest LS range
                            bestLSRange=availableCorrHists[closestRunWithCorr][0]

                        print "Closest match with correction is",closestRunWithCorr,bestLSRange
                        histSuffix=str(closestRunWithCorr)+"_LS"+str(bestLSRange[0])+"_LS"+str(bestLSRange[1])
                        thisCorrHist=corrtfile.Get("Ratio_Correction_"+histSuffix)
                        allCorrHist=corrtfile.Get("Overall_Ratio_"+histSuffix)
                except:
                    print "No correction for",tree.run,tree.ls
            else:
                thisCorrHist=0
                allCorrHist=0
            #print tree.nCluster,
            #print tree.run,
            #print NBXPerFill[thisFill],
            #print tree.LS
            #nClusterXNBX=tree.nCluster*NBXPerRun[tree.run]
            nClusterXNBX=tree.nCluster*NBXPerFill[thisFill]
            PCLumi_uncorr=nClusterXNBX*f_LHC/args.xsec
            PCLumi_corr=PCLumi_uncorr
            corrFactor=1.0
            if corrPerFill.has_key(thisFill):
                corrFactor=corrPerFill[thisFill]
            #print tree.run,thisFill,NBXPerFill[thisFill],corrFactor
            if allCorrHist!=0:
                #print "corrFactor, Before",corrFactor
                #print "getbin",allCorrHist.GetBinContent(1)
                if allCorrHist.GetBinContent(1)>0.8:
                    corrFactor=allCorrHist.GetBinContent(1)
                    #print "corrFactor, After",corrFactor
                
            rawPCCFile.write(str(tree.run)+","+str(tree.LS)+","+str(nClusterXNBX*corrFactor)+"\n")
            if args.xing==1:
                rawPCCFilePerBX.write(str(tree.run)+","+str(tree.LS)+","+str(nClusterXNBX*corrFactor))
                for ibx in range(1,3565):
                    if ibx not in tree.PCBXid:
                        rawPCCFilePerBX.write(","+str(0.0))
                    else:
                        index=list(tree.PCBXid).index(ibx)
                        if thisCorrHist!=0:
                            rawPCCFilePerBX.write(","+str(tree.nPCPerBXid[index]*(1-thisCorrHist.GetBinContent(ibx+1))))
                        else:
                            rawPCCFilePerBX.write(","+str(tree.nPCPerBXid[index]))
                rawPCCFilePerBX.write("\n")
            print "correction factor:", corrFactor
            PCLumi_corr=PCLumi_corr*corrFactor
            PCLumiFile.write(str(tree.run)+","+str(tree.LS)+","+str(PCLumi_corr)+"\n")
            if args.xing==1:
                PCLumiFilePerBX.write(str(tree.run)+","+str(tree.LS)+","+str(PCLumi_corr))
                for ibx in range(1,3565):
                    if ibx not in tree.PCBXid:
                        PCLumiFilePerBX.write(","+str(0.0))
                    else:
                        index=list(tree.PCBXid).index(ibx)
                        if thisCorrHist!=0:
                            PCLumiFilePerBX.write(","+str(tree.nPCPerBXid[index]*(1-thisCorrHist.GetBinContent(ibx+1))))
                        else:
                            PCLumiFilePerBX.write(","+str(tree.nPCPerBXid[index]))
                PCLumiFilePerBX.write("\n")
            else:
                print "No corrections available for run",thisFill,tree.run
                print "DO NOTHING... CORRECTIONS ARE REQUIRED"
            lastFill=thisFill
        tfile.Close()
    except:
        print "Problem with file",filename
        try:
            tfile.Close()
        except:
            print "Can't even close it"

rawPCCFile.close()
PCLumiFile.close()
if args.xing==1:
    rawPCCFilePerBX.close()
    PCLumiFilePerBX.close()
