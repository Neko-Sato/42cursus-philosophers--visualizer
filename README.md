# 42cursus-philosophers--visualizer

## 使い方

シミュレーションを開始する前にこの関数を呼びます
```
philovisualizer_init([哲学者とフォークの数]);
```

哲学者の状態が変化する度にこの関数を呼びます
```
//	PV_THINKING
//	PV_EATING
//	PV_SLEEPING
//	PV_DIED
//	PV_TAKE_LEFT
//	PV_PUT_LEFT
//	PV_TAKE_RIGHT
//	PV_PUT_RIGHT

philovisualizer_send([哲学者の番号], [上のいずれか])
```

バックグラウンドで実行してから実行します
```
./philo_visualizer.py &
./philo ...
```
