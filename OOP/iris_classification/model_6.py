from __future__ import annotations
import pytest
from model import TrainingKnownSample, UnknownSample
from model import CD, ED, MD, SD
from typing import Tuple, TypedDict


class ED(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return hypot(
            s1.sepal_length - s2.sepal_length,
            s1.sepal_width - s2.sepal_width,
            s1.petal_length - s2.petal_length,
            s1.petal_width - s2.petal_width,
        )


        @pytest.fixture
        def known_unknown_example_15() -> Known_Unknown:
            known_row: Row = {
                "species": "Iris-setosa",
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            }
            k = TrainingKnownSample(**known_row)
            unknown_row = {
                "sepal_length": 7.9,
                "sepal_width": 3.2,
                "petal_length": 4.7,
                "petal_width": 1.4,
            }
            u = UnknownSample(**unknown_row)
            return k, u

        def test_ed(known_unknown_example_15: Known_Unknown) -> None:
            k, u = known_unknown_example_15
            assert ED().distance(k, u) == pytest.approx(4.50111097)

        def test_cd(known_unknown_example_15: Known_Unknown) -> None:
            k, u = known_unknown_example_15
            assert CD().distance(k, u) == pytest.approx(3.3)

        def test_md(known_unknown_example_15: Known_Unknown) -> None:
            k, u = known_unknown_example_15
            assert MD().distance(k, u) == pytest.approx(7.6)

        def test_sd(known_unknown_example_15: Known_Unknown) -> None:
            k, u = known_unknown_example_15
            assert SD().distance(k, u) == pytest.approx(0.277372263)


Known_Unknown = Tuple[TrainingKnownSample, UnknownSample]
class Row(TypedDict):
    species: str
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

""" Unit testing the Hyperparameter class """
from unittest.mock import Mock, sentinel, call

class Hyperparameter:

    def __init__(
        self,
        k: int,
        algorithm: "Distance",
        training: "TrainingData"
    ) -> None:
        self.k = k
        self.algorithm = algorithm
        self.data: weakref.ReferenceType["TrainingData"] = \
            weakref.ref(training)
        self.quality: float

    def classify(
        self,
        sample: Union[UnknownSample, TestingKnownSample]) -> str:
        """The k-NN algorith"""
        training_data = self.data()
        if not training_data:
            raise RuntimeError("No TrainingData object")
        distances: list[tuple[float, TrainingKnownSample]] = sorted(
            (self.algorithm.distance(sample, known), known)
            for known in training_data.training
        )
        k_nearest = (known.species for d, known in distances[: self.k])
        frequency: Counter[str] = collections.Counter(k_nearest)
        best_fit, *others = frequency.most_common()
        species, votes = best_fit
        return species

    @pytest.fixture
    def sample_data() -> list[Mock]:
        return [
            Mock(name="Sample1", species=sentinel.Species3),
            Mock(name="Sample2", species=sentinel.Species1),
            Mock(name="Sample3", species=sentinel.Species1),
            Mock(name="Sample4", species=sentinel.Species1),
            Mock(name="Sample5", species=sentinel.Species3),
        ]

    @pytest.fixture
    def hyperparameter(sample_data: list[Mock]) -> Hyperparameter:
        mocked_distance = Mock(distance=Mock(side_effect=[11, 1, 2, 3, 13]))
        mocked_training_data = Mock(training=sample_data)
        mocked_weakref = Mock(
            return_value=mocked_training_data)
        fixture = Hyperparameter(
            k=3, algorithm=mocked_distance, training=sentinel.Unused)
        fixture.data = mocked_weakref
        return fixture

    def test_hyperparameter(sample_data: list[Mock], hyperparameter: Mock) -> None:
        s = hyperparameter.classify(sentinel.Unknown)
        assert s == sentinel.Species1
        assert hyperparameter.algorithm.distance.mock_calls == [
            call(sentinel.Unknown, sample_data[0]),
            call(sentinel.Unknown, sample_data[1]),
            call(sentinel.Unknown, sample_data[2]),
            call(sentinel.Unknown, sample_data[3]),
            call(sentinel.Unknown, sample_data[4]),
        ]

    def test(self) -> "Hyperparameter":
        """Run the entire test suite."""
        pass_count, fail_count = 0, 0
        for sample in self.data.testing:
            sample.classification = self.calssify(sample)
            if sample.matches():
                pass_count += 1
            else:
                fail_count += 1
        self.quality = pass_count / (pass_count + fail_count)
        return self

    def grid_search_1() -> None:
        td = TrainingData("Iris")
        source_path = Path.cwd().parent / "bezdekiris.data"
        reader = CSVIrisReader(source_path)
        td.load(reader.data_iter())

        tuning_results: List[Hyperparameter] = []
        with futures.ProcessPoolExecutor(8) as workers:
            test_runs: List[futures.Future[Hyperparameter]] = []
            for k in range(1, 41, 2):
                for algo in ED(), MD(), CD(), SD():
                    h = Hyperparameter(k, algo, td)
                    test_runs.append(workers.submit(h.test))
            for f in futures.as_completed(test_runs):
                tuning_results.append(f.result())
        for result in tuning_results:
            print(
                f"{result.k:2d} {result.algorithm.__class__.__name__:2s}"
                f" {result.quality:.3f}"
            )
#
""" Concurrency """

for k in range(1, 41, 2):
    for algo in ED(), MD(), CD(), SD():
        h = Hyperparameter(k, algo, td)
        print(h.test())
