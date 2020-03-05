import typing
from .utils import cartesian_product


class R3D3Experiment(typing.NamedTuple):
    config: typing.Dict
    binary: str


class R3D3ExperimentPlan(typing.NamedTuple):
    experiments: typing.List[R3D3Experiment]
    max_nb_processes: int
    db_path: str

    @classmethod
    def from_cartesian_space(
        cls, db_path: str, configs: typing.Dict, binary: str, max_nb_processes: int
    ) -> "R3D3ExperimentPlan":

        experiments = [
            R3D3Experiment(binary=binary, config=config)
            for config in cartesian_product(configs)
        ]

        return cls(
            experiments=experiments, max_nb_processes=max_nb_processes, db_path=db_path
        )
