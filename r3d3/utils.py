import typing


def cartesian_product(grid: typing.Dict):
    """
    Helper function to compute the cartesian product
    of an experiment grid.
    For instance the grid
        {
            a: ['a1', 'a2', 'a3'],
            b: ['b1', 'b2']
        }
    will produce
        [
            {a: 'a1', b:'b1'},
            {a: 'a2', b:'b2'},
            {a: 'a3', b:'b1'},
            {a: 'a1', b:'b2'},
            {a: 'a2', b:'b1'},
            {a: 'a3', b:'b2'}
        ]
    """
    my_keys = list(grid.keys())

    configs = [{my_keys[0]: val} for val in grid[my_keys[0]]]

    print(configs)

    for key in my_keys[1:]:
        my_values = grid[key]
        new_configs = list()
        for config in configs:
            for value in my_values:
                new_configs.append({key: value, **config})
        configs = new_configs

    return configs


def namedtuple_to_dict(input: typing.NamedTuple) -> typing.Dict:
    root = input._asdict()
    my_stash = [root]
    while len(my_stash) > 0:
        subroot = my_stash.pop()
        for key in subroot:
            if hasattr(subroot[key], "_asdict"):
                subroot[key] = subroot[key]._asdict()
                my_stash.append(subroot[key])
    return root


def dict_to_param_map(input_dict: typing.Dict):
    my_stack = list()

    all_paths = list()

    for key in input_dict:
        my_stack.append(([key], input_dict[key]))

    while len(my_stack) > 0:
        current_path, current_config = my_stack.pop()
        if current_config is None:
            all_paths.append(current_path)
        else:
            for key in current_config:
                my_stack.append((current_path + [key], current_config[key]))

    config = dict()
    for path in all_paths:
        config["_".join(path)] = ".".join(path)

    return config
