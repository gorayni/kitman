import json
from functools import reduce
from operator import truediv
from pathlib import Path

import numpy as np

from kitman.data import DirPathsBuilder
from kitman.field_calibration import format_homography


leagues_abbv = {'england_epl': 'ENG',
                'europe_uefa-champions-league': 'UCL',
                'france_ligue-1': 'FRA',
                'germany_bundesliga': 'GER',
                'italy_serie-a': 'ITA',
                'spain_laliga': 'SPA'}

team_abbv = {'1. FSV Mainz 05': 'M05',
             'AC Milan': 'ACM',
             'AS Roma': 'ASR',
             'Ajax': 'AJX',
             'Alaves': 'ALV',
             'Almeria': 'ALM',
             'Anderlecht': 'AND',
             'Angers': 'ANG',
             'Arsenal': 'ARS',
             'Aston Villa': 'AVL',
             'Atalanta': 'ATA',
             'Ath Bilbao': 'ATHB',
             'Atl. Madrid': 'ATM',
             'Atletico Madrid': 'ATM',
             'Augsburg': 'AUG',
             'B. Monchengladbach': 'BMG',
             'BATE': 'BAT',
             'Barcelona': 'BAR',
             'Basel': 'BASEL',
             'Bastia': 'BAS',
             'Bayer Leverkusen': 'B04',
             'Bayern': 'BAY',
             'Bayern Munich': 'BAY',
             'Benfica': 'BEN',
             'Besiktas': 'BES',
             'Betis': 'BET',
             'Bologna': 'BOL',
             'Bordeaux': 'BORDX',
             'Borussia': 'BOR',
             'Bournemouth': 'BOU',
             'Burnley': 'BUR',
             'CSKA Moscow': 'CSKA',
             'Caen': 'CAE',
             'Cagliari': 'CAG',
             'Celta Vigo': 'CELV',
             'Celtic': 'CEL',
             'Chelsea': 'CHE',
             'Chievo': 'CHI',
             'Cordoba': 'COR',
             'Crotone': 'CRO',
             'Crystal Palace': 'CRY',
             'D. Zagreb': 'DIN',
             'Darmstadt': 'DAR',
             'Dep. La Coruna': 'DEP',
             'Dijon': 'DIJ',
             'Dortmund': 'BVB',
             'Dyn. Kiev': 'DYN',
             'Eibar': 'EIB',
             'Eintracht Frankfurt': 'EIN',
             'Elche': 'ELC',
             'Empoli': 'EMP',
             'Espanyol': 'ESP',
             'Everton': 'EVE',
             'FC Astana': 'AST',
             'FC Augsburg': 'FCA',
             'FC Koln': 'FCK',
             'FC Porto': 'FCP',
             'Fiorentina': 'FIO',
             'Frankfurt': 'FRA',
             'Frosinone': 'FRO',
             'Galatasaray': 'GAL',
             'Genoa': 'GEN',
             'Gent': 'GENT',
             'Getafe': 'GET',
             'Gijon': 'GIJ',
             'Granada': 'GRA',
             'Granada CF': 'GCF',
             'Guingamp': 'GUI',
             'Hamburger': 'HAM',
             'Hamburger SV': 'HSV',
             'Hertha': 'HER',
             'Hertha Berlin': 'BSC',
             'Hoffenheim': 'HOF',
             'Hull City': 'HUL',
             'Ingolstadt': 'ING',
             'Inter': 'INT',
             'Internazionale': 'INT',
             'Juventus': 'JUV',
             'Las Palmas': 'PAL',
             'Lazio': 'LAZ',
             'Leganes': 'LEG',
             'Leicester': 'LEI',
             'Leipzig': 'RBL',
             'Levante': 'LEV',
             'Lille': 'LIL',
             'Liverpool': 'LIV',
             'Lorient': 'LOR',
             'Ludogorets': 'LUD',
             'Ludogorets Razgrad': 'LUDR',
             'Lyon': 'LYO',
             'Maccabi Tel Aviv': 'MTA',
             'Malaga': 'MAL',
             'Malmo FF': 'MFF',
             'Manchester City': 'MCI',
             'Manchester United': 'MUN',
             'Marseille': 'MAR',
             'Metz': 'MET',
             'Middlesbrough': 'MID',
             'Monaco': 'MON',
             'Montpellier': 'MONT',
             'Nancy': 'NANCY',
             'Nantes': 'NAN',
             'Napoli': 'NAP',
             'Newcastle Utd': 'NEW',
             'Nice': 'NIC',
             'Norwich': 'NOR',
             'Olympiakos Piraeus': 'OLY',
             'Osasuna': 'OSA',
             'PSV': 'PSV',
             'Paderborn': 'PAD',
             'Palermo': 'PALRM',
             'Paris SG': 'PSG',
             'Pescara': 'PES',
             'RB Leipzig': 'RBL',
             'Rayo Vallecano': 'RAY',
             'Real Madrid': 'RMD',
             'Real Sociedad': 'RSO',
             'Reims': 'REI',
             'Rennes': 'REN',
             'SC Freiburg': 'SCF',
             'SV Werder Bremen': 'SVW',
             'Saint Etienne': 'STE',
             'Sampdoria': 'SAM',
             'Sassuolo': 'SAS',
             'Schalke': 'S04',
             'Sevilla': 'SEV',
             'Shakhtar Donetsk': 'SHA',
             'Southampton': 'SOU',
             'St Etienne': 'STE',
             'Stoke City': 'STK',
             'Sunderland': 'SUN',
             'Swansea': 'SWA',
             'Torino': 'TOR',
             'Tottenham': 'TOT',
             'Toulouse': 'TOU',
             'Udinese': 'UDI',
             'Valencia': 'VAL',
             'Verona': 'VER',
             'VfB Stuttgart': 'VFB',
             'Villarreal': 'VIL',
             'Watford': 'WAT',
             'West Brom': 'WBA',
             'West Ham': 'WHU',
             'Wolfsburg': 'WOB',
             'Zenit Petersburg': 'ZEN'}


def shorten_name(match: Path):
    league = leagues_abbv[match.parts[-3]]
    date = match.parts[-1][2:10]
    time = f'{match.parts[-1][13:15]}{match.parts[-1][16:18]}'

    score = match.parts[-1][19:]
    team1, team2 = score.split(' - ')
    score1, team1 = team1[-1:], team_abbv[team1[:-2]]
    score2, team2 = team2[:1], team_abbv[team2[2:]]

    return f'{league}_{date}_{time}_{team1}_{score1}-{score2}_{team2}'


def load_scaling_matrix(sars_filepath: Path):
    with sars_filepath.open(mode='r') as f:
        sampling_aspect_ratio = reduce(truediv, map(float, f.readline().split(':')))

    scaling_matrix = np.identity(3)
    if sampling_aspect_ratio > 1:
        scaling_matrix[0, 0] = 1 / sampling_aspect_ratio
    return scaling_matrix


def load_homographies(calibration_filepath: Path, transformation_matrix: np.ndarray = None):
    with calibration_filepath.open() as json_file:
        data = json.load(json_file)

    homographies = []
    for prediction in data['predictions']:
        homography_matrix = format_homography(prediction[0]['homography'])
        if transformation_matrix is not None:
            homography_matrix = homography_matrix @ transformation_matrix
        homographies.append({'matrix': homography_matrix,
                             'confidence': prediction[0]['confidence']})
    return homographies


def load_groundtruth_bboxes(bboxes_filepath: Path):
    with bboxes_filepath.open() as json_file:
        data = json.load(json_file)
    return data['predictions']


class FrameIndex:
    def __init__(self, half, frame_idx):
        self.half = half
        self.frame_idx = frame_idx


class MatchPaths(DirPathsBuilder):
    def __init__(self, match_path):
        super().__init__(match_path, {'calibrations': '{}_field_calib_ccbv.json',
                                      'frames': ['{}_HQ', 'frames', '{:05d}.jpg'],
                                      'groundtruth': 'segmentations.npy',
                                      'predicted_segmentations': 'predicted_segmentation_{}.npy',
                                      'predicted_segmentations_bkg': 'predicted_segmentation_bkg_{}.npy',
                                      'sampling_aspect_ratio': 'sampling_aspect_ratio.txt',
                                      'segmentations': 'segmentation_results_{}_HQ.npy'
                                      })
        self.match = match_path
