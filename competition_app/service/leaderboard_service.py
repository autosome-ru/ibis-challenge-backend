from numpy import arange, random

from competition_app.constants import stages, methods, disciplines, disciplines_tfs_matrices, all_disciplines, all_tfs


# hereafter only generators

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


# hereafter only generators for development purposes

def get_ranks(metrics_matrix):
    ranks_matrix = ((-metrics_matrix).argsort(0)).argsort(0)
    print(metrics_matrix)
    print(ranks_matrix)
    return ranks_matrix


def get_aggregated_ranks(ranks_matrix, proportion=2):
    num_rows, num_cols = ranks_matrix.shape
    weights = ((arange(num_cols) + 1) + (proportion - 1) * num_cols) / (proportion * num_cols)
    return (-ranks_matrix * weights).sum(axis=1).argsort(0)


def generate_team_submits(discipline_name, tf_name, submit_max_amount=10, metrics_amount=3):
    discipline_id = all_disciplines.index(discipline_name)
    tf_id = all_tfs.index(tf_name)

    tf_total = len(all_tfs)
    discipline_total = len(all_disciplines)
    random.seed(discipline_total * tf_id + discipline_id)
    submit_amount = random.randint(0, submit_max_amount)
    metrics_values = random.rand(submit_amount, metrics_amount)
    metrics_ranks = get_ranks(metrics_values)
    aggregated_ranks = get_aggregated_ranks(metrics_ranks)
    submits = []

    metrics_order = ['metric_' + str(val) for val in list(range(metrics_amount))]

    for i in range(submit_amount):
        submits.append({
            'id': i,
            'name': 'name %d' % i,
            'info': 'Comment for submit # %d' % i,
            'metrics': metrics_values[i].tolist(),
            'ranks': metrics_ranks[i].tolist(),
            'team': 'Team %d' % i,
            'aggregated_rank': aggregated_ranks[i]
        })

    # return {
    #     'metrics_order': ["Metric name #" + str(val) for val in list(range(metrics_amount))],
    #     'submits': submits,
    #     'discipline_name': all_disciplines[discipline_id],
    #     'tf_name': all_tfs[tf_id]
    # }
    return {'metrics_order': metrics_order, 'submits': submits}
