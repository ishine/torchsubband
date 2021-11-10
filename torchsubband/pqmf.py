#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pqmf.py    
@Contact :   haoheliu@gmail.com
@License :   (C)Copyright 2020-2100

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
9/19/21 4:11 PM   Haohe Liu      1.0         None
'''
import torch
import torch.nn.functional as F
import torch.nn as nn
import os.path as op
from scipy.io import loadmat
import numpy as np

filters = {
    "f_2_64": np.array([[ 1.44449283e-04,  1.20348353e-04,  2.44166250e-04,
         4.04000633e-04, -7.56150315e-05, -2.60371593e-04,
         3.67984707e-06,  1.98684879e-04,  5.88149971e-04,
        -2.75148674e-05, -9.16297506e-04,  2.51955388e-04,
         6.75673071e-04, -9.04202825e-04, -1.07195960e-03,
         2.76842647e-03,  3.04375641e-03, -6.19007748e-03,
        -5.80496493e-03,  1.07917069e-02,  7.20738980e-03,
        -1.64295966e-02, -5.83826196e-03,  2.53039261e-02,
         2.07530180e-04, -4.31940824e-02,  1.48379847e-02,
         7.92414235e-02, -4.94480507e-02, -1.57710291e-01,
         2.16162487e-01,  8.78782935e-01,  9.88625361e-01,
         3.20296171e-01, -2.71622918e-01, -1.43512952e-01,
         1.80781878e-01,  9.52334887e-02, -1.50333693e-01,
        -7.39523979e-02,  1.27597289e-01,  5.72774705e-02,
        -1.02818498e-01, -4.13218270e-02,  7.61031431e-02,
         2.65769546e-02, -5.06773713e-02, -1.54838574e-02,
         3.07731394e-02,  8.93061461e-03, -1.80700580e-02,
        -5.31425229e-03,  1.06233974e-02,  3.39814456e-03,
        -6.72627764e-03, -1.60449351e-03,  3.91349535e-03,
         3.28266738e-04, -1.80153044e-03, -2.02849870e-04,
         3.11579316e-04,  4.59042075e-04, -8.98816676e-04,
        -4.81008119e-05],
       [-2.46304629e-04, -4.31599907e-04, -7.79763302e-04,
        -9.18891970e-04, -2.33353681e-04, -6.71909410e-04,
         9.39021643e-05,  5.82736213e-04, -2.64174549e-05,
        -3.99773808e-04,  2.92325531e-05,  7.40896111e-04,
         2.66399818e-04, -2.34511161e-03, -1.29585458e-03,
         6.16755821e-03,  2.82091580e-03, -1.09433837e-02,
        -4.26695709e-03,  1.46822376e-02,  6.27032061e-03,
        -1.74829403e-02, -1.25126866e-02,  2.15109726e-02,
         2.89976948e-02, -2.83783740e-02, -6.28788743e-02,
         3.77083994e-02,  1.40876704e-01, -4.32312962e-02,
        -5.61500056e-01,  1.04590217e+00, -7.13874656e-01,
        -5.01983305e-02,  2.83138492e-01,  4.70376933e-02,
        -1.94458244e-01, -4.74314566e-02,  1.58497132e-01,
         4.76432898e-02, -1.28990760e-01, -4.19289164e-02,
         9.66905703e-02,  3.08697492e-02, -6.55720002e-02,
        -1.93765804e-02,  4.06279971e-02,  1.08567996e-02,
        -2.38104642e-02, -5.67906563e-03,  1.42658984e-02,
         3.49706425e-03, -8.49313742e-03, -2.67488248e-03,
         4.91439995e-03,  1.84441516e-03, -2.53678789e-03,
        -8.08817682e-04,  5.22858599e-04, -6.14193406e-05,
        -8.66801157e-04, -1.51132587e-04,  3.43542085e-04,
         3.16309575e-05]]),
    "f_4_64": np.array([[ 1.20157946e-04,  2.15395242e-04, -7.27477137e-04,
        -9.99397525e-04,  1.89855741e-04,  6.30797666e-04,
         2.01384833e-03,  2.09264271e-03,  1.21702278e-03,
         3.36934919e-05, -1.10067244e-02, -1.26220772e-02,
         2.08317501e-03,  1.25878831e-02,  2.78221847e-02,
         2.63322307e-02,  8.90653821e-03, -2.41430929e-02,
        -7.91172396e-02, -8.44201493e-02, -3.01278975e-03,
         6.60624819e-02,  1.39250822e-01,  1.15436331e-01,
         9.84058735e-03, -1.46874606e-01, -2.74719391e-01,
        -2.18705176e-01,  6.07491047e-02,  4.48974376e-01,
         8.65962454e-01,  1.10740837e+00,  1.05933431e+00,
         7.89015438e-01,  3.72272721e-01,  6.60882154e-03,
        -1.84329463e-01, -1.99182053e-01, -7.27260366e-02,
         5.63492913e-02,  1.05546415e-01,  9.28771373e-02,
         2.15090209e-02, -3.93351340e-02, -5.48533397e-02,
        -3.68010135e-02, -2.19538530e-02,  3.44325213e-02,
         3.70222238e-02,  4.16529927e-02, -2.29467335e-02,
        -1.00565142e-02, -1.35091103e-02, -1.98153381e-02,
         9.94130080e-03,  1.21679506e-03,  5.14654533e-03,
         6.98693248e-03, -4.53453498e-03,  1.70002322e-03,
        -9.13661680e-04, -1.98875979e-03,  8.86840706e-04,
        -9.72819699e-04],
       [-6.02137575e-04, -1.23433295e-03,  4.04403432e-03,
         7.83202133e-03, -2.52533421e-03, -6.17959847e-03,
        -7.83501252e-03, -4.48788864e-03, -1.34492533e-02,
        -1.48071857e-02,  7.24266690e-02,  1.03330882e-01,
        -1.61895210e-02, -9.48370510e-02, -9.25170571e-02,
        -2.53197919e-02, -1.35371296e-01, -1.67716986e-02,
         4.31287615e-01,  5.81746878e-01, -7.93917015e-02,
        -6.33182630e-01, -3.32035939e-01,  5.28469427e-02,
        -2.09594385e-01, -6.22777284e-02,  1.01154816e+00,
         1.18993278e+00, -5.98714131e-01, -1.88481705e+00,
        -6.20456088e-01,  1.25267293e+00,  1.05614988e+00,
        -3.35771681e-01, -5.43999583e-01,  1.70630933e-01,
         1.63794791e-01, -2.70681797e-01, -2.01754435e-01,
         1.30657695e-01,  1.52916948e-01, -9.69749045e-03,
        -4.55914783e-04,  2.07542508e-02, -5.63688770e-02,
        -2.95879611e-02,  2.45576720e-02,  1.02298647e-02,
         2.11932727e-02,  2.20993349e-02, -1.05872467e-02,
         3.97789452e-03, -1.38331041e-02, -5.00088471e-03,
         9.23233297e-03, -7.55790540e-03,  2.28507392e-03,
         1.76400532e-03, -1.45897563e-03,  1.60644777e-03,
        -5.28946650e-04,  3.66826685e-04,  9.28642130e-05,
        -4.10759606e-04],
       [ 1.49069567e-03,  1.59040352e-03, -3.45473122e-03,
        -6.12779772e-03,  6.54634319e-04,  6.83642014e-03,
        -6.92427729e-03, -3.07838349e-05,  2.95288496e-02,
         1.10283174e-02, -2.81976058e-02, -6.32992560e-02,
         3.22378944e-02,  7.54747766e-02, -1.21757618e-01,
         1.53969689e-02,  1.44827699e-01,  6.97028441e-02,
        -1.16610343e-01, -2.97350249e-01,  3.92522599e-01,
         2.74201757e-01, -6.60349684e-01,  1.26301179e-01,
         4.80680928e-01, -4.15437489e-02, -3.18124428e-01,
        -5.75119005e-01,  1.06708621e+00,  5.17326365e-01,
        -1.94471021e+00,  7.54508946e-01,  1.52477880e+00,
        -1.60466738e+00, -1.56923978e-01,  9.20260785e-01,
        -3.49205733e-01,  1.29593724e-01, -2.76885406e-01,
        -8.19309552e-02,  6.72617775e-01, -4.36592172e-01,
        -2.30716707e-01,  3.94047428e-01, -1.39996630e-01,
         8.72534905e-03,  1.16482143e-02, -8.03711881e-02,
         1.25476136e-01, -5.50954311e-02, -5.18545436e-02,
         7.23346250e-02, -2.08200097e-02,  2.24620359e-03,
         7.83935370e-03, -1.44716673e-02,  8.91796204e-03,
        -3.29182380e-03, -3.52683420e-03,  5.87272538e-03,
        -1.46977944e-03,  3.41322987e-04,  8.05121653e-04,
        -1.01374416e-03],
       [ 2.20725357e-04,  4.98439615e-04,  6.02671273e-05,
        -5.03234287e-04, -1.17562897e-03,  8.85526904e-04,
        -1.16242406e-03, -1.38398522e-03,  4.90945684e-03,
         1.66153106e-03,  1.01161710e-02, -4.81975455e-03,
        -9.68805501e-04,  9.84832671e-03, -1.96919682e-02,
         1.01802514e-02, -1.16425995e-02,  2.55237734e-02,
         3.49231421e-02, -5.75244384e-02,  9.47189173e-03,
         2.87060284e-02, -6.66576088e-02,  5.75078886e-02,
         4.06273742e-02, -1.52225517e-01,  1.95429657e-01,
        -8.05818492e-02, -2.29631960e-01,  6.15972996e-01,
        -9.38350608e-01,  1.07982690e+00, -9.52893946e-01,
         6.30985350e-01, -2.48870237e-01, -8.43699157e-02,
         2.08591167e-01, -1.81583951e-01,  8.13494152e-02,
         8.13630530e-02, -1.27650934e-01,  9.75206758e-02,
        -4.83724824e-02, -4.70829267e-02,  7.50834818e-02,
        -4.56959454e-02,  1.02322939e-02,  2.30439560e-02,
        -4.65752388e-02, -1.51293591e-02,  1.22392187e-02,
        -2.05764607e-03,  2.20860846e-02,  5.86533195e-03,
        -1.23526109e-02,  7.03124779e-03, -5.17105657e-03,
        -4.55498777e-03,  4.25069355e-03, -2.21507234e-03,
         1.80952580e-03,  7.63541042e-04, -1.01998309e-03,
         1.67674370e-03]]),
    "f_8_64": np.array([[ 1.06684581e-02, -9.37053746e-03, -7.87581010e-03,
         1.46133318e-03, -4.90685741e-04, -1.52055172e-02,
         6.97099823e-03,  2.86526797e-03,  1.65083771e-02,
        -1.67435856e-02, -1.01513693e-03, -8.82422581e-03,
        -2.24523237e-02, -3.08467132e-03, -1.64270681e-02,
        -2.07550852e-02,  1.87427520e-02,  3.65588237e-02,
         3.74738349e-02,  3.59202663e-02,  4.25332269e-02,
         2.66160967e-02, -2.42169559e-02, -4.94641076e-02,
         4.35551267e-02,  8.03624690e-02,  1.09547899e-01,
         2.71527588e-01,  4.64177003e-01,  6.38220013e-01,
         8.61670363e-01,  9.91850600e-01,  1.05878270e+00,
         1.08106796e+00,  1.04738446e+00,  9.27340330e-01,
         7.22209668e-01,  5.43269021e-01,  2.83455507e-01,
         3.70375516e-02, -9.77588097e-02, -2.76744725e-01,
        -3.19640109e-01, -3.30615639e-01, -2.90115473e-01,
        -1.92607576e-01, -8.68163292e-02, -5.60017896e-04,
         4.72087173e-02,  7.86277281e-02,  8.51174986e-02,
         8.83093690e-02,  7.14405137e-02,  5.02976235e-02,
         2.76948168e-02,  4.98384230e-03, -3.84396291e-02,
        -3.40830797e-03, -9.33888546e-03, -5.18367471e-03,
        -1.56053501e-02, -8.37070802e-03,  6.67527805e-03,
         1.96227457e-03],
       [ 7.40172350e-03, -5.98442009e-03, -5.65178476e-03,
         4.63523339e-03,  8.16036508e-04, -4.27024719e-03,
         8.07466408e-03,  1.25245399e-03,  1.54805393e-02,
        -5.37105341e-03,  2.94234792e-03,  8.22737521e-03,
        -6.60656034e-03, -9.62267674e-04, -1.86079927e-03,
        -1.30121764e-02,  3.09529237e-02, -4.63400574e-03,
        -2.42753849e-02,  2.42691475e-02, -2.59088328e-02,
        -9.24146422e-02, -2.12662402e-02,  2.72271838e-02,
        -2.11578530e-02, -1.30548671e-01, -2.50595765e-01,
        -3.23594883e-01, -2.43859773e-01,  1.35333855e-01,
         5.46858166e-01,  8.57163345e-01,  9.89389367e-01,
         6.62443631e-01,  4.00305655e-02, -6.24084804e-01,
        -1.09886114e+00, -1.20919748e+00, -8.93330751e-01,
        -2.97590909e-01,  3.29416968e-01,  6.90936044e-01,
         7.55680495e-01,  5.37547665e-01,  2.12039980e-01,
         1.29980496e-02, -8.89054579e-02, -1.02185357e-01,
         4.73622187e-02,  2.02278307e-03, -2.11099700e-03,
        -5.39051585e-02, -1.26415932e-01, -1.35933458e-01,
        -6.64145256e-02,  1.49147451e-02,  2.78368734e-02,
         6.02791208e-02,  1.14821012e-02,  1.44388205e-02,
         2.42796759e-02, -5.31322349e-03, -7.45466066e-03,
        -8.10091314e-04],
       [ 8.24540643e-03, -6.31635019e-03,  4.00343951e-03,
        -2.90229288e-05,  1.09743831e-02, -1.52713857e-02,
         2.17286395e-03, -2.30429213e-03,  9.99386093e-03,
        -1.87627466e-02, -4.21837057e-02,  3.42327622e-02,
        -2.08975937e-02, -3.40070393e-03,  8.86945783e-03,
         7.37941159e-02,  1.30865495e-03,  3.69162812e-04,
        -6.85514498e-02, -1.35594425e-01, -1.64710103e-02,
        -1.79219933e-02, -2.46890812e-02, -8.22632691e-03,
         1.02946232e-01,  2.89343288e-01,  2.25562496e-01,
        -1.18499090e-01, -5.54731147e-01, -6.12593442e-01,
         4.91894041e-02,  8.21907840e-01,  9.34709083e-01,
         1.27254562e-01, -8.61958285e-01, -1.12300743e+00,
        -3.20568733e-01,  7.36793736e-01,  1.05108361e+00,
         4.45321798e-01, -5.08993634e-01, -8.34525822e-01,
        -4.29872195e-01,  1.80321141e-01,  4.88426559e-01,
         1.84959401e-01, -3.68903758e-02, -1.54393556e-02,
        -4.00066715e-02,  2.72646065e-03, -9.68830692e-02,
        -1.34144368e-01, -2.41865847e-02,  1.11933350e-01,
         1.13531553e-01,  2.81597564e-02, -8.20054800e-02,
        -8.17201227e-02, -2.94093805e-03,  1.28013340e-02,
        -1.81999282e-02,  9.05556421e-03,  1.89518739e-02,
        -3.23183137e-03],
       [-4.09568738e-04,  2.00155658e-03,  9.35790520e-03,
        -5.87190409e-03,  3.64102660e-03,  1.30938931e-04,
        -2.86051062e-03, -6.81837477e-03, -1.43137999e-02,
         2.78879155e-02,  9.07702381e-03,  1.61015851e-03,
        -3.35699104e-02,  5.52201203e-02,  1.93265500e-02,
        -2.42605206e-03,  2.16737806e-02, -4.77361145e-02,
        -1.15153737e-01,  3.10106748e-02,  6.18410869e-02,
        -1.23110639e-02,  5.44497961e-02,  1.70135410e-02,
        -1.26758813e-01, -2.10417565e-01,  7.28434858e-02,
         4.20903518e-01,  5.07850076e-02, -6.86462378e-01,
        -4.07949789e-01,  7.21209521e-01,  7.62525593e-01,
        -5.06254476e-01, -1.10244288e+00,  8.72485964e-02,
         1.13256456e+00,  3.03954292e-01, -9.87855534e-01,
        -6.38732771e-01,  6.12230751e-01,  7.49031400e-01,
        -2.39571519e-01, -6.13037136e-01, -5.06809749e-02,
         3.40405811e-01,  6.47505918e-02, -8.24823858e-02,
        -2.54535001e-02, -8.61050285e-02, -1.07533964e-01,
         2.37612109e-02,  1.68205457e-01,  2.32659855e-02,
        -1.04605074e-01, -5.98552503e-02,  5.40038730e-02,
         7.78542076e-02, -5.05534112e-02, -2.61672399e-02,
         2.26868413e-02, -4.36188881e-03, -6.52064688e-03,
        -1.28485327e-02],
       [ 1.86971518e-03,  2.07198394e-02,  2.15498014e-02,
        -8.99573408e-03, -3.01878872e-02,  5.57082603e-02,
         1.28531393e-02, -7.26138643e-02,  6.13790572e-02,
        -7.99797922e-02, -1.29805957e-01,  1.42213764e-01,
         5.06780643e-02, -1.69955426e-01,  5.85138933e-02,
         1.78394727e-01, -2.15955684e-01, -8.49013752e-02,
         3.22181783e-01, -1.93661517e-01, -1.91576376e-01,
         3.79611693e-01, -1.46839328e-01, -4.33222893e-01,
         5.46205587e-01,  2.28208235e-01, -7.46628005e-01,
         2.20844903e-01,  8.50234066e-01, -6.64308423e-01,
        -6.25890850e-01,  9.43030970e-01,  2.93919542e-01,
        -1.05886554e+00,  6.73892800e-02,  9.41898761e-01,
        -3.43403661e-01, -7.12082081e-01,  3.91308749e-01,
         4.30145359e-01, -3.45478246e-01, -3.07201787e-01,
         2.95265304e-01,  2.69822161e-01, -1.88377285e-01,
        -2.40610447e-01,  2.11264167e-01,  2.26907696e-01,
        -1.58240099e-01, -1.17520745e-01,  1.09992820e-01,
         7.58066580e-02, -1.11986581e-01, -3.39857070e-02,
         9.02062258e-02,  5.81880982e-02, -4.65905212e-02,
        -3.37738537e-02,  1.51094013e-02,  2.03570459e-02,
        -2.33815873e-02, -1.28079683e-02,  1.59852176e-02,
         2.06575615e-03],
       [-5.18634408e-03, -3.42411458e-02, -1.45088285e-02,
        -9.74416148e-03,  5.51182654e-02, -8.41097621e-02,
        -3.70961115e-03,  1.06662612e-01, -8.98778625e-02,
         5.85474285e-02,  1.53081296e-01, -1.96775163e-01,
         4.37851647e-02,  6.57602205e-02, -1.31426774e-01,
         1.48225629e-02,  2.53633360e-02,  2.34863583e-01,
        -2.15590120e-01, -7.73706790e-02,  5.75956672e-01,
        -5.89171174e-01, -3.95486150e-02,  8.73317207e-01,
        -9.62321609e-01,  1.87388308e-02,  9.11392736e-01,
        -1.08588714e+00,  2.71129763e-01,  7.64957738e-01,
        -1.09909562e+00,  3.80593056e-01,  5.34736803e-01,
        -8.39814487e-01,  4.41042939e-01,  2.25440645e-01,
        -4.47688057e-01,  2.63800377e-01,  4.03403343e-02,
        -1.24305829e-01,  1.01276496e-01, -3.25259631e-02,
         5.66138786e-02, -3.34967568e-02, -1.01866138e-02,
        -1.74600316e-02, -1.16033638e-01,  1.41287537e-02,
         4.47430977e-02,  1.57554264e-02,  7.60305642e-03,
        -3.76467615e-03,  2.36795485e-02,  2.07347466e-02,
        -2.41257487e-02,  1.62999784e-02, -1.74337841e-02,
        -1.39627180e-03, -8.24274979e-03,  5.06866046e-03,
        -6.36540574e-03, -6.05196333e-03,  6.27237420e-03,
        -3.05771066e-03],
       [ 1.51416659e-02, -2.76282993e-03,  1.99382817e-02,
        -1.51933989e-02, -2.36193651e-03,  1.08962990e-02,
         1.71992766e-02, -6.80104705e-02,  8.58673186e-02,
        -1.74592384e-02, -1.10475719e-01,  1.65392931e-01,
        -1.58296700e-01,  1.19998845e-01,  3.52952164e-02,
        -1.19671950e-01,  1.49646357e-01, -1.55923675e-01,
        -6.81116136e-02,  2.72091826e-01, -2.70011262e-01,
         1.88096327e-02,  4.12597162e-01, -6.38757930e-01,
         7.08665228e-01, -4.76155561e-01, -1.30234016e-01,
         7.09737108e-01, -1.10950570e+00,  1.12452339e+00,
        -7.02027739e-01,  3.83735304e-02,  5.74041288e-01,
        -9.10814490e-01,  9.40190207e-01, -6.90525612e-01,
         2.81556710e-01,  9.14447821e-02, -2.40730055e-01,
         3.85142398e-01, -3.41379317e-01,  2.73073101e-01,
        -2.61721030e-01,  1.46306051e-01, -5.64109567e-02,
         1.93672248e-02,  1.11815749e-01, -1.70774622e-01,
         1.25662256e-01, -6.96457051e-02,  6.06282236e-02,
        -3.12800475e-02, -1.03824975e-02,  1.60887622e-02,
        -5.60561514e-02,  2.15733000e-02, -7.84947999e-03,
         2.02298601e-02, -1.89814013e-02, -4.15700957e-03,
         1.19317111e-02,  2.75417912e-03, -9.01277418e-04,
        -3.69346877e-03],
       [ 3.28231555e-03, -9.03208761e-03,  1.14567260e-02,
        -1.16651666e-02,  1.32922372e-02, -1.06059815e-02,
        -6.48731157e-03, -1.13975687e-02, -2.22654465e-02,
         7.49907312e-04, -2.34458468e-02,  3.51489543e-02,
        -3.83469525e-02,  5.22572276e-02, -3.89955421e-02,
         4.85307907e-02, -1.91809129e-02, -5.07836875e-03,
         7.14158028e-02, -1.39002852e-01,  1.78563565e-01,
        -1.56125576e-01,  1.58412517e-01, -9.63230568e-02,
        -1.42871453e-02,  1.76779571e-01, -3.69354977e-01,
         5.84655914e-01, -7.90981020e-01,  9.30169295e-01,
        -1.04540896e+00,  1.09487377e+00, -1.08599346e+00,
         9.90227634e-01, -8.52728831e-01,  6.73174935e-01,
        -4.60833637e-01,  2.31252165e-01, -2.78327451e-02,
        -1.15618081e-01,  1.90389353e-01, -2.39826051e-01,
         2.31414981e-01, -1.66111419e-01,  1.30906402e-01,
        -4.33249929e-02, -5.13408107e-02,  1.25279191e-01,
        -1.17096178e-01,  9.49992863e-02, -8.66870658e-02,
         5.13403004e-02, -6.51721580e-03, -2.86115031e-02,
         2.78979996e-02, -2.65072379e-02,  5.92663963e-02,
        -2.60527429e-02,  4.07427567e-02,  2.42220410e-03,
        -1.17435656e-02,  6.59993194e-03, -1.40492002e-02,
         1.49743245e-02]]),
    "h_2_64": np.array([[-6.00608122e-06, -2.84725573e-04,  1.95528907e-04,
        -4.60117098e-04,  3.26082641e-04, -2.80381596e-04,
         1.25856947e-04,  2.69082582e-04, -3.64133774e-04,
        -6.43926682e-04,  3.43313122e-04,  1.39237138e-03,
        -2.69118955e-04, -2.40824156e-03,  6.68994725e-04,
         3.68490863e-03, -2.31457351e-03, -5.38147890e-03,
         5.18557404e-03,  8.19634569e-03, -8.74648742e-03,
        -1.31380018e-02,  1.33746216e-02,  2.07606019e-02,
        -2.07071352e-02, -3.12315675e-02,  3.36310153e-02,
         4.76588870e-02, -6.24529942e-02, -9.31415237e-02,
         1.51530978e-01,  4.57469167e-01,  4.45213257e-01,
         1.37143136e-01, -7.95800099e-02, -4.83700921e-02,
         3.91223531e-02,  2.26742974e-02, -2.04641276e-02,
        -4.69436519e-03,  8.64078965e-03, -5.41488708e-03,
        -1.34219136e-03,  8.14484885e-03, -1.41663688e-03,
        -6.34081543e-03,  1.20993506e-03,  3.06946397e-03,
        -9.18394386e-05, -4.84028090e-04, -8.35891746e-04,
        -4.12812218e-04,  8.88143396e-04,  4.19397775e-04,
        -4.63484883e-04, -2.12997109e-04,  5.23474014e-05,
         1.39504214e-04,  2.29977779e-04, -2.49979200e-04,
         2.20408236e-04, -1.63484878e-05,  1.06628310e-04,
         1.42225182e-04],
       [ 1.15157525e-05,  8.58854370e-05, -4.15161920e-05,
        -8.70073272e-05,  5.29844131e-05, -1.07217870e-04,
         1.00869141e-04, -1.15999990e-04,  1.91458939e-04,
         4.20501353e-04, -5.50359684e-04, -8.32440405e-04,
         8.61837945e-04,  1.17587362e-03, -1.31528818e-03,
        -1.97770482e-03,  1.48707664e-03,  4.38068500e-03,
        -1.25972928e-03, -8.99691323e-03,  1.18577673e-03,
         1.55252363e-02, -2.09551980e-03, -2.40279500e-02,
         3.63188520e-03,  3.63823504e-02, -3.76189664e-03,
        -5.76350715e-02,  2.18099974e-03,  1.06254477e-01,
        -2.40182423e-03, -3.24373285e-01,  5.03665197e-01,
        -3.06256439e-01, -5.17031177e-03,  8.71799569e-02,
         3.09698044e-03, -4.31895025e-02, -4.05492769e-03,
         1.89190240e-02,  6.30167519e-03, -3.23456539e-03,
        -7.97652122e-03, -4.76038002e-03,  7.75505702e-03,
         6.45974215e-03, -5.46056956e-03, -4.25717264e-03,
         2.65383165e-03,  1.18261296e-03, -8.02407891e-04,
         6.45955306e-04, -1.65256354e-05, -1.17253203e-03,
         1.03700134e-04,  5.47099819e-04, -1.48655621e-04,
         1.10494215e-05,  1.43453702e-04,  1.01967783e-04,
        -2.50741279e-04, -1.70382258e-04, -2.28933266e-04,
        -1.98390036e-04]]),
    "h_4_64": np.array([[ 3.45932142e-05, -5.08269979e-05, -1.62409926e-04,
         1.10403325e-04, -2.67986266e-04,  2.59791427e-04,
         5.76079041e-04, -2.06672143e-04,  9.43991693e-05,
         3.05396163e-04, -2.44752731e-03,  1.58574695e-03,
        -1.02310753e-04, -2.06400732e-03,  6.69166377e-04,
        -8.17224055e-04, -7.60839248e-04,  6.99743344e-03,
         1.71026988e-03, -4.78395778e-03, -4.80162170e-03,
         1.91356974e-03,  1.36102838e-02,  1.30875806e-02,
        -2.02525375e-03, -2.15889215e-02, -3.75041635e-02,
        -2.71880228e-02,  2.38187174e-02,  1.03573735e-01,
         1.88054303e-01,  2.44019270e-01,  2.49457126e-01,
         2.01575656e-01,  1.18278250e-01,  3.09635651e-02,
        -2.98183071e-02, -5.11376204e-02, -3.64767830e-02,
        -9.51134521e-03,  1.15979963e-02,  2.15157902e-02,
         9.75058006e-03, -1.11094870e-04, -2.97077296e-03,
        -7.18908061e-03, -2.08878961e-03, -3.77833386e-03,
         8.68806259e-04,  5.52301325e-05,  2.13233871e-03,
         1.56309672e-03, -7.00510966e-04,  6.80881574e-04,
        -5.37886749e-04,  5.80643140e-04,  3.45325037e-04,
        -4.48519486e-04, -7.45724256e-05, -4.00082884e-04,
        -2.15748810e-04,  2.37716653e-04,  4.13445642e-05,
         2.52053417e-04],
       [ 1.15935776e-05,  3.36974435e-05, -1.01654298e-04,
        -9.52342533e-05,  2.28381995e-05,  1.35120100e-04,
         1.91322305e-04, -5.23648248e-05, -3.07171588e-04,
        -2.37012537e-04,  4.68674801e-04,  1.53324289e-03,
        -7.24461452e-04, -2.27552547e-03, -1.08108152e-03,
         1.67578686e-03,  3.58364833e-03,  1.62349838e-03,
        -4.80133116e-03, -1.28518305e-02,  7.69230119e-03,
         1.57139482e-02,  1.16369660e-02, -1.10145595e-02,
        -2.48504467e-02,  2.32186857e-05,  3.46186879e-02,
         2.34894230e-02, -3.43194936e-02, -7.11823534e-02,
        -1.17240017e-02,  1.07584997e-01,  1.16870531e-01,
        -4.37404428e-02, -1.72660705e-01, -8.92010216e-02,
         9.60784261e-02,  1.37039047e-01,  2.40636279e-02,
        -5.72799165e-02, -3.86274771e-02, -1.59446684e-02,
        -1.83837604e-02,  3.95795558e-03,  2.85177502e-02,
         2.12786112e-02, -6.46760047e-03, -1.31842193e-02,
        -9.51180565e-04, -4.10347085e-03, -1.68635591e-03,
         3.03961552e-03,  1.20665119e-04,  6.18454547e-03,
        -3.38929796e-04,  1.90546559e-03,  7.30175660e-04,
        -1.63621484e-03,  1.87635903e-04, -1.01832058e-03,
        -4.85032276e-04,  6.04939933e-04,  2.29402445e-04,
         7.32018478e-04],
       [ 2.28405502e-07, -6.73275994e-05,  5.82437483e-05,
         8.19800608e-05, -1.54076872e-04, -5.78242198e-05,
         2.71336854e-04,  1.34782948e-06, -4.36071301e-04,
         1.12366237e-03, -8.71016627e-04, -1.18935909e-03,
         2.46039477e-03, -1.67547580e-04, -3.49265103e-03,
         2.17480314e-03,  3.75746557e-03, -7.42963670e-03,
         7.72377514e-03,  2.45885740e-03, -1.23584651e-02,
        -1.27444532e-03,  1.41870988e-02,  1.43503862e-03,
        -3.49851107e-02,  3.85718664e-02,  1.00532001e-02,
        -7.83663475e-02,  8.14645277e-02,  1.35562436e-02,
        -1.32834680e-01,  1.09297004e-01,  5.69277350e-02,
        -1.57350195e-01,  5.63747309e-02,  9.64449878e-02,
        -9.06496594e-02, -2.44429617e-02,  5.68585102e-02,
         1.62164514e-03, -2.51994996e-02,  2.24430192e-04,
         1.57512106e-02, -6.85928678e-03,  1.23685172e-03,
         8.23216609e-03, -1.46933437e-02,  3.47592285e-03,
         6.90514132e-03, -4.47522399e-03, -1.89058114e-03,
        -3.78019136e-03, -1.28306608e-03, -6.48796093e-05,
         3.62472695e-04, -1.57065019e-04,  2.59871453e-04,
        -1.67885722e-06,  8.16526127e-05, -3.25171877e-04,
         6.21972546e-06,  1.84672799e-04, -4.50535988e-06,
         1.53710018e-04],
       [-1.04654371e-04,  1.03126627e-04,  7.45513571e-05,
        -4.60049008e-05, -8.15794492e-06,  3.44860950e-05,
        -4.41382293e-04,  2.61257804e-04,  1.07692409e-03,
        -1.82343057e-03, -3.50274360e-04,  1.45065551e-03,
        -1.80415854e-03,  3.02505355e-03,  3.77477940e-03,
        -7.89416733e-03,  5.08505884e-04,  5.39359444e-03,
        -1.08159118e-02,  1.74135172e-02, -6.02209343e-03,
        -1.13771279e-02,  2.91771477e-02, -2.89746221e-02,
         1.21707012e-02,  2.02804103e-02, -4.77534398e-02,
         5.12060475e-02, -1.17630495e-02, -6.55981999e-02,
         1.59589432e-01, -2.32320782e-01,  2.59816845e-01,
        -2.31612307e-01,  1.54663109e-01, -6.58979902e-02,
        -9.19858319e-03,  4.70710425e-02, -4.35016676e-02,
         2.12680520e-02,  5.53774816e-03, -2.12996095e-02,
         1.51654440e-02, -3.68926098e-03, -8.26935656e-03,
         1.23603926e-02, -8.12071092e-03, -3.43884114e-03,
         3.38128128e-03, -1.12718763e-02,  2.11003331e-03,
        -3.87257955e-03, -3.19862018e-03,  4.35048293e-03,
        -4.06025776e-04,  3.54786093e-03,  1.30827689e-03,
        -1.57852149e-03, -2.44982999e-04, -1.59657569e-03,
        -2.61166680e-04,  4.42782465e-04,  6.44744170e-05,
         4.25145295e-04]]),
    "h_8_64": np.array([[-3.41011019e-04,  1.36338764e-04, -3.00861831e-04,
        -1.86669081e-03, -7.44063425e-05, -9.44075111e-05,
        -2.34624036e-03, -3.91815776e-03,  3.67099563e-03,
         2.77394411e-03,  5.81176454e-03,  9.90459777e-03,
         7.64989808e-03,  6.24183639e-03,  1.17762811e-02,
         8.42980545e-03, -4.08235240e-03, -1.19796926e-02,
        -2.48511276e-02, -3.09441580e-02, -3.97926911e-02,
        -4.08260505e-02, -2.94330774e-02, -1.09178606e-02,
         3.14268924e-03,  3.14620141e-02,  6.69928911e-02,
         9.26737697e-02,  1.14487973e-01,  1.27848004e-01,
         1.32943002e-01,  1.31831178e-01,  1.25418141e-01,
         1.05106594e-01,  8.24496868e-02,  6.28748439e-02,
         3.72549193e-02,  1.36402146e-02,  8.66959543e-03,
         3.88052216e-03, -4.18650729e-03, -3.04895975e-03,
         1.47634145e-03,  6.01673198e-03,  3.45824554e-03,
         3.05680077e-03,  2.49282508e-03, -4.96521662e-04,
         8.95276904e-04,  1.93709165e-04, -2.56831069e-04,
        -7.47588809e-04, -2.39769826e-03,  6.62595671e-04,
        -1.53629711e-03,  5.83237349e-04, -1.82118026e-04,
         3.31375034e-04, -1.09859130e-03,  2.95267602e-04,
        -8.20718338e-04, -2.41462820e-05, -5.56013363e-04,
         5.43529557e-04],
       [ 3.97164251e-04, -2.46155019e-03, -1.84532474e-03,
         1.76556072e-03,  7.98757274e-04, -3.32784002e-04,
         8.70488836e-03,  5.81487925e-03, -4.90008465e-03,
        -1.74768464e-02, -1.83133306e-02, -1.34295288e-02,
         1.87653461e-03,  5.62709329e-03,  8.99398785e-03,
         6.19774677e-03, -1.95240810e-02, -2.14448521e-02,
        -2.25697193e-03,  2.19395449e-02,  6.97792323e-02,
         9.43032877e-02,  8.02360643e-02,  3.46817682e-02,
        -3.70766682e-02, -1.02675492e-01, -1.44687560e-01,
        -1.33162550e-01, -7.40136731e-02,  6.01089469e-03,
         7.74684405e-02,  1.17586625e-01,  1.09841634e-01,
         7.00348002e-02,  1.50492678e-02, -3.41870825e-02,
        -4.77936745e-02, -3.98099196e-02, -1.35310373e-02,
         4.24821963e-03,  8.52691063e-03,  5.48311258e-03,
        -8.36610858e-03, -1.05407192e-02, -5.12057567e-03,
        -9.84076957e-03,  9.89576981e-04,  8.52328428e-03,
        -1.64269870e-04,  1.17668009e-03,  4.84735636e-04,
        -1.51157471e-03, -3.03916665e-03,  3.19644887e-03,
         8.32656677e-04,  3.07473274e-04,  1.97796625e-04,
         4.98780529e-05, -1.21556967e-04,  7.38506661e-04,
        -3.37104242e-04,  1.49553404e-04, -8.00851519e-05,
        -5.17514930e-05],
       [-1.27394554e-03,  1.68076334e-03,  5.57113822e-04,
        -1.00293174e-03,  4.32519103e-03,  2.05598987e-03,
        -8.52714803e-03, -1.11086675e-02,  8.31923811e-03,
         1.43580677e-02,  4.26746265e-03, -3.48358557e-03,
        -1.63114378e-02, -1.00150512e-02,  6.11044492e-03,
         2.39522348e-03, -2.77547519e-03,  1.54833110e-03,
         2.40516969e-02,  5.06509389e-02,  1.78737598e-02,
        -6.11501984e-02, -1.02839434e-01, -5.15348990e-02,
         6.14604872e-02,  1.35242746e-01,  9.19681683e-02,
        -4.64957598e-02, -1.45787815e-01, -1.15002104e-01,
         6.63580524e-03,  1.12364780e-01,  1.13036019e-01,
         1.79782836e-02, -7.13233057e-02, -7.53002475e-02,
        -2.44672473e-02,  2.63836090e-02,  3.13929973e-02,
         4.12672575e-03, -2.77539041e-03, -4.72615939e-03,
         8.46355287e-03,  2.61690670e-03, -1.92877626e-02,
        -8.05898360e-03,  1.34299573e-03, -2.53406957e-04,
         3.23432130e-03,  1.22890161e-03,  2.31817915e-03,
        -1.50714762e-03,  1.21089751e-03, -8.42759749e-04,
        -8.48033002e-04,  4.74411720e-04,  2.23209765e-04,
         1.43697855e-05, -1.62377658e-03,  8.93134330e-04,
        -2.67003518e-04,  7.43978844e-04, -1.65263519e-04,
         3.21471799e-05],
       [-5.66721158e-04, -2.47708060e-03, -4.44897372e-04,
         3.86713037e-03, -6.29995669e-03, -8.25844335e-03,
         1.05226046e-02,  9.38149284e-03, -1.13802854e-02,
        -1.64975312e-02,  6.90468918e-03,  1.74554264e-02,
        -7.11219863e-04, -1.22573432e-02, -9.90748561e-03,
         3.02517002e-04, -1.37118400e-02,  7.50372870e-03,
         4.00219937e-02, -7.99938199e-03, -6.78860075e-02,
        -2.71694077e-02,  9.35465224e-02,  7.27962795e-02,
        -8.48023627e-02, -1.23627500e-01,  4.34637020e-02,
         1.55464987e-01,  1.71053631e-02, -1.43077548e-01,
        -6.64128106e-02,  1.00767058e-01,  9.04061547e-02,
        -5.01193126e-02, -8.26028524e-02,  3.71430582e-03,
         5.87466867e-02,  1.37775178e-02, -1.88563351e-02,
        -1.25564783e-02,  4.17859934e-03,  1.17773595e-03,
        -1.87740852e-03,  1.18773956e-02,  1.65830550e-03,
        -1.00092418e-02, -7.16219300e-03,  2.23876359e-03,
         2.11628062e-03,  6.68838234e-03,  2.46612438e-03,
        -1.78810876e-03,  5.06850617e-04, -9.97885899e-04,
         1.44008315e-03,  2.70442506e-03, -1.08438701e-03,
         1.05353212e-03,  8.09129677e-05, -1.98618695e-04,
        -1.26588137e-03,  1.30148316e-03,  4.75564652e-04,
        -3.34056882e-05],
       [-1.26964311e-03,  4.89905472e-05, -8.52583782e-04,
        -1.67061597e-03,  4.10090195e-03,  2.46437119e-03,
        -5.15396314e-03, -5.30307562e-03,  1.48095065e-03,
         1.10685920e-02, -6.10388606e-03, -1.00264447e-02,
         1.60108197e-02,  1.39127346e-02, -1.31229416e-02,
        -2.64495164e-02,  3.00248204e-02,  2.66041639e-02,
        -3.33549577e-02, -1.64874885e-02,  3.25037386e-02,
         3.54651844e-02, -3.15755978e-02, -4.57926444e-02,
         4.93697649e-02,  5.11510981e-02, -8.83578095e-02,
        -5.31311821e-02,  1.21437533e-01,  1.20639224e-02,
        -1.41633467e-01,  4.37332411e-02,  1.22501885e-01,
        -8.77316173e-02, -7.79478882e-02,  1.14736236e-01,
         2.22167982e-02, -9.94035816e-02,  3.14704444e-02,
         5.82983503e-02, -5.46818028e-02, -9.79058764e-03,
         4.29338258e-02, -2.90486578e-02, -1.42739371e-02,
         4.08815358e-02, -1.65368367e-02, -2.52169019e-02,
         1.91106798e-02,  7.85145368e-03, -1.83168195e-02,
         8.46951935e-03,  1.04453098e-02, -1.24734262e-02,
        -2.20846912e-03,  8.11961416e-03, -6.35633850e-03,
         2.46374594e-03,  4.21811682e-03, -3.11720197e-03,
        -8.52779622e-04,  1.21147349e-03,  1.02238887e-03,
         8.65513621e-04],
       [-8.73213908e-04,  3.24142573e-04, -5.56910613e-04,
         5.10179859e-05,  1.09391038e-03,  2.38374681e-04,
        -1.09587172e-03, -1.83095628e-03,  1.60138419e-03,
         2.46433820e-03, -1.50236720e-03,  6.71428054e-04,
        -4.07252757e-03, -1.30358311e-03,  4.70945446e-03,
         4.98836109e-03,  3.45551085e-03, -1.24612872e-02,
        -6.23334540e-04,  7.39603716e-03, -4.33708758e-03,
        -2.50102580e-03,  1.22855371e-04,  1.28183230e-02,
        -1.51609160e-02,  6.42362547e-03,  3.37308183e-02,
        -5.56444430e-02,  2.49752088e-02,  6.43298954e-02,
        -1.05701639e-01,  5.48114886e-02,  6.69940289e-02,
        -1.42417534e-01,  8.98700461e-02,  3.96133977e-02,
        -1.39059157e-01,  1.13145132e-01,  5.83811945e-03,
        -1.11085588e-01,  1.07151723e-01, -1.88267897e-02,
        -5.92969976e-02,  6.33265611e-02, -1.76214998e-02,
        -1.15423366e-02,  2.59814415e-02, -3.45056813e-03,
        -7.71224774e-04, -1.51262083e-02,  6.65825927e-03,
         5.67538379e-03, -1.47573411e-02,  1.64177034e-02,
         1.15063796e-03, -8.83854173e-03,  8.38770640e-03,
         1.86166058e-03, -4.73762524e-03,  6.36688669e-03,
         1.81334458e-05, -1.50411081e-03, -2.76612417e-03,
         4.39017920e-04],
       [-4.62900904e-04,  6.26326898e-04, -3.22606480e-05,
         2.37621520e-03, -3.16868128e-03, -3.35535319e-03,
         3.41435556e-03,  1.77470304e-03,  3.23304775e-04,
        -6.17387682e-03,  4.89992815e-03, -4.68518614e-04,
        -2.07985714e-03,  4.87543981e-03, -1.06621796e-02,
         1.16635977e-02, -1.83653237e-02,  1.12338856e-02,
         4.96727981e-03, -9.76751355e-03,  8.63137773e-03,
        -2.10988741e-02,  2.57877843e-02, -4.07528257e-02,
         5.18272996e-02, -3.75089393e-02,  1.41448516e-02,
         3.33447204e-02, -8.59191981e-02,  1.16663374e-01,
        -1.08175756e-01,  6.23390327e-02,  1.23503165e-02,
        -8.82667989e-02,  1.32091668e-01, -1.27727007e-01,
         8.21537110e-02, -1.56341175e-02, -5.98403695e-02,
         8.77569276e-02, -8.65336323e-02,  5.27075348e-02,
         1.76043779e-03, -3.28956725e-02,  3.15576853e-02,
        -1.96640245e-02, -1.29201130e-02,  2.40563727e-02,
        -2.39420468e-02,  6.59156129e-03,  1.37889804e-02,
        -2.38413849e-02,  2.33162066e-02, -1.67015422e-02,
        -5.15680219e-05,  1.12879249e-02, -8.58068718e-03,
         4.17647190e-03, -7.80789427e-04, -3.16749925e-03,
         3.01491173e-03, -5.90353244e-04, -1.30831417e-03,
         3.73774321e-03],
       [ 2.70795665e-03, -1.49939914e-03,  1.09795607e-03,
        -3.16351715e-03,  1.24825122e-03,  6.07409183e-03,
        -3.12466036e-03,  4.03868851e-03, -1.95227520e-03,
         3.09385391e-03, -2.90025707e-03, -9.31360559e-04,
         3.39854838e-03, -4.22768641e-03,  9.65637233e-03,
        -1.23930301e-02,  6.83751198e-03, -1.58886661e-03,
        -3.11535089e-03,  1.30619171e-02, -1.59218831e-02,
         2.13692165e-02, -2.54832687e-02,  2.07499401e-02,
        -5.60690708e-03, -7.66889534e-03,  2.70441409e-02,
        -5.54831727e-02,  8.04173774e-02, -1.01075485e-01,
         1.18178389e-01, -1.29911767e-01,  1.35170866e-01,
        -1.28926919e-01,  1.15943695e-01, -9.68445884e-02,
         7.28578436e-02, -4.48990791e-02,  2.65948239e-02,
        -6.13152879e-03, -6.06338993e-03,  1.38909243e-02,
        -2.07786559e-02,  1.90168423e-02, -1.72115909e-02,
         1.00132177e-02, -1.44761326e-03,  4.93224894e-05,
         4.46078874e-03, -4.40033964e-03,  4.48673298e-03,
        -1.82489283e-03,  9.13957359e-04, -2.76075737e-03,
         1.82116009e-03, -3.56297273e-03, -2.46820105e-03,
         1.08700238e-03, -1.54145720e-03, -2.27237024e-04,
         6.10636148e-04, -2.99996332e-04, -5.75750889e-04,
         6.46664273e-04]]),
}

def load_mat2numpy(fname=""):
    '''
    Args:
        fname: pth to mat
        type:
    Returns: dic object
    '''
    if (len(fname) == 0):
        return None
    else:
        return loadmat(fname)

class PQMF(nn.Module):
    def __init__(self, N, M):
        super().__init__()
        self.N = N  # nsubband
        self.M = M  # nfilter
        try:
            assert (N, M) in [(8, 64), (4, 64), (2, 64)]
        except:
            print("Warning:", N, "subbandand ", M, " filter is not supported")
        self.pad_samples = 64
        self.name = str(N) + "_" + str(M)
        self.ana_conv_filter = nn.Conv1d(1, out_channels=N, kernel_size=M, stride=N, bias=False)
        data = filters["f_" + self.name]
        data = data.astype(np.float32) / N
        data = np.flipud(data.T).T
        data = np.reshape(data, (N, 1, M)).copy()
        dict_new = self.ana_conv_filter.state_dict().copy()
        dict_new['weight'] = torch.from_numpy(data)
        self.ana_pad = nn.ConstantPad1d((M - N, 0), 0)
        self.ana_conv_filter.load_state_dict(dict_new)

        self.syn_pad = nn.ConstantPad1d((0, M // N - 1), 0)
        self.syn_conv_filter = nn.Conv1d(N, out_channels=N, kernel_size=M // N, stride=1, bias=False)
        gk = filters["h_" + self.name]
        gk = gk.astype(np.float32)
        gk = np.transpose(np.reshape(gk, (N, M // N, N)), (1, 0, 2)) * N
        gk = np.transpose(gk[::-1, :, :], (2, 1, 0)).copy()
        dict_new = self.syn_conv_filter.state_dict().copy()
        dict_new['weight'] = torch.from_numpy(gk)
        self.syn_conv_filter.load_state_dict(dict_new)

        for param in self.parameters():
            param.requires_grad = False

    def __analysis_channel(self, inputs):
        return self.ana_conv_filter(self.ana_pad(inputs))

    def __systhesis_channel(self, inputs):
        ret = self.syn_conv_filter(self.syn_pad(inputs)).permute(0, 2, 1)
        return torch.reshape(ret, (ret.shape[0], 1, -1))

    def analysis(self, inputs):
        '''
        :param inputs: [batchsize,channel,raw_wav],value:[0,1]
        :return:
        '''
        batch, channels, samples = inputs.shape
        inputs = F.pad(inputs,((0,self.pad_samples)))
        inputs = inputs.view(-1, 1, samples)
        ret = self.__analysis_channel(inputs).view(batch, channels, -1)
        return ret

    def synthesis(self, data):
        '''
        :param data: [batchsize,self.N*K,raw_wav_sub],value:[0,1]
        :return:
        '''
        ret = None
        batch, _, samples = data.shape
        ret = self.__systhesis_channel(data.view(-1, self.N, samples))
        ret = ret.view(batch, -1, ret.shape[2])[...,:-self.pad_samples]
        return ret

    def forward(self, inputs):
        return self.ana_conv_filter(self.ana_pad(inputs))
