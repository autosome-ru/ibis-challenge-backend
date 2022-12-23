from pandas import read_csv
import json

roles = ('ADMIN', 'TEAM-SPOKESMAN')

stages = ('leaderboard', 'final')
methods = ('AAA', 'PWM')
all_methods = ('AAA', 'PWM', 'ALL')
disciplines_tfs_matrices = {
    'leaderboard': {},
    'final': {}
}
disciplines_tfs_matrices['leaderboard']['AAA'] = read_csv("competition_app/data/leaderboard_AAA_map.csv",
                                                          index_col=0)
disciplines_tfs_matrices['leaderboard']['PWM'] = read_csv("competition_app/data/leaderboard_PWM_map.csv",
                                                          index_col=0)
disciplines_tfs_matrices['final']['AAA'] = read_csv("competition_app/data/final_AAA_map.csv",
                                                    index_col=0)
disciplines_tfs_matrices['final']['PWM'] = read_csv("competition_app/data/final_PWM_map.csv",
                                                    index_col=0)

disciplines = {
    'leaderboard':
        {
            'AAA': disciplines_tfs_matrices['leaderboard']['AAA'].columns.tolist(),
            'PWM': disciplines_tfs_matrices['leaderboard']['PWM'].columns.tolist()
        },
    'final':
        {
            'AAA': disciplines_tfs_matrices['final']['AAA'].columns.tolist(),
            'PWM': disciplines_tfs_matrices['final']['PWM'].columns.tolist()
        },
    'all': {}
}
all_disciplines = tuple(set(disciplines['leaderboard']['AAA'] +
                            disciplines['final']['AAA'] +
                            disciplines['leaderboard']['PWM'] +
                            disciplines['final']['PWM']))

tfs = {
    'leaderboard':
        {
            'AAA': disciplines_tfs_matrices['leaderboard']['AAA'].index.tolist(),
            'PWM': disciplines_tfs_matrices['leaderboard']['PWM'].index.tolist()
        },
    'final':
        {
            'AAA': disciplines_tfs_matrices['final']['AAA'].index.tolist(),
            'PWM': disciplines_tfs_matrices['final']['PWM'].index.tolist()
        },
    'all': {}
}
all_tfs = tuple(set(tfs['leaderboard']['AAA'] +
                    tfs['final']['AAA'] +
                    tfs['leaderboard']['PWM'] +
                    tfs['final']['PWM']))


def get_disciplines_tf_map():
    result = {}
    for stage in stages:
        result[stage] = {}
        for method in methods:
            result[stage][method] = {}
            for discipline in disciplines[stage][method]:
                selected = disciplines_tfs_matrices[stage][method][discipline]
                result[stage][method][discipline] = \
                    tuple(selected[selected].index.values)
    return result


def get_disciplines_tf_array():
    result = []
    for stage in stages:
        for method in methods:
            for discipline in disciplines[stage][method]:
                selected = disciplines_tfs_matrices[stage][method][discipline]
                result.append(
                    {
                        "stage": stage,
                        "method": method,
                        "discipline": discipline,
                        "tfs": list(selected[selected].index.values)
                    }
                )
    return result


# print(get_disciplines_tf_array())
# challenge_general_info = {
#     'stages': stages,
#     'methods': methods,
#     'disciplines': disciplines,
#     'tfs': tfs,
#     'disciplines_tfs_map': get_disciplines_tf_map(),
#     'tfs_info':
#         {
#             'names': all_tfs,
#             'view': [x + " view" for x in all_tfs],
#             'comment': [x + " comment" for x in all_tfs]
#         },
#     'disciplines_info':
#         {
#             'names': all_disciplines,
#             'view': [x + " view" for x in all_disciplines],
#             'comment': [x + " comment" for x in all_disciplines]
#         }
# }

disciplines_general_info = read_csv("competition_app/data/disciplines_description.csv").fillna('')
tfs_general_info = read_csv("competition_app/data/tfs_description.csv").fillna('')
methods_description = [
    {
        "name": "AAA",
        "view": "AAA",
        "comment": ""
    },
    {
        "name": "PWM",
        "view": "PWM",
        "comment": ""
    }
]

metrics = ["first", "second", "third"]
discipline_metrics = [{'discipline': discipline, "metrics": metrics} for discipline in all_disciplines]

challenge_general_info = {
    # 'methods': methods_description,
    'disciplines': list(disciplines_general_info.T.to_dict().values()),
    'tfs': list(tfs_general_info.T.to_dict().values()),
    'metrics': discipline_metrics
}

tfs['all']['AAA'] = list(set(tfs['leaderboard']['AAA'] + tfs['final']['AAA']))
tfs['all']['PWM'] = list(set(tfs['leaderboard']['PWM'] + tfs['final']['PWM']))
disciplines['all']['AAA'] = list(set(disciplines['leaderboard']['AAA'] + disciplines['final']['AAA']))
disciplines['all']['PWM'] = list(set(disciplines['leaderboard']['PWM'] + disciplines['final']['PWM']))
