#include <iostream>
#include <cmath>
#include <chrono>
#include <omp.h>

using namespace std;
using namespace std::chrono;

// функція для обчислення відстані між двома n-вимірними векторами
double distance(double* x, double* y, int n, int p) {
    double result = 0.0;
    if (p == -1) { // норма L-безкінечність
        for (int i = 0; i < n; i++) {
            double diff = abs(x[i] - y[i]);
            if (diff > result) {
                result = diff;
            }
        }
    }
    else { // норма L-p
        for (int i = 0; i < n; i++) {
            result += pow(abs(x[i] - y[i]), p);
        }
        result = pow(result, 1.0 / p);
    }
    return result;
}

int main() {
    setlocale(LC_ALL, "Russian");
    const int n = 100000;
    const int p = 2;
    double* x = new double[n];
    double* y = new double[n];
    for (int i = 0; i < n; i++) {
        x[i] = (double)rand() / RAND_MAX;
        y[i] = (double)rand() / RAND_MAX;
    }
    
    // послідовне обчислення
    double result_serial;
    high_resolution_clock::time_point start_serial = high_resolution_clock::now(); // запустити таймер
    result_serial = distance(x, y, n, p);
    high_resolution_clock::time_point end_serial = high_resolution_clock::now(); // таймер завершення
    duration<double> time_serial = duration_cast<duration<double>>(end_serial - start_serial); // розрахувати різницю в часі

    cout << "Результат розв'язку завдання: " << result_serial << endl;
    cout << "Час виконання в однопотоковому режимi: " << time_serial.count() << " секунд" << endl;
    
    // паралельне обчислення з різною кількістю потоків
    int num_threads[] = { 2, 4, 6, 8, 10, 20 };
    for (int i = 0; i < 6; i++) {
        double result_parallel;
        high_resolution_clock::time_point start_parallel = high_resolution_clock::now(); // запустити таймер
        omp_set_num_threads(num_threads[i]); // встановити кількість потоків
#pragma omp parallel
        {
            result_parallel = distance(x, y, n, p); // обчислюємо відстань паралельно
        }
        high_resolution_clock::time_point end_parallel = high_resolution_clock::now(); // таймер завершення
        duration<double> time_parallel = duration_cast<duration<double>>(end_parallel - start_parallel); // розрахувати різницю в часі

        cout << "Час виконання в режимi з " << num_threads[i] << " потоками: " << time_parallel.count() << " секунд" << endl;
    }

    delete[] x;
    delete[] y;

    return 0;
}