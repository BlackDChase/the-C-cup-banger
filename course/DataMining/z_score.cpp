#include <bits/stdc++.h>
using namespace std;


int main()
{
    int n;
    cout << "Enter the number of elements : ";
    cin >> n;

    vector <double> v(n), ans(n);
    double sum = 0;
    cout << "Enter the elements " << endl;

    for(int i = 0; i < n; i++)
    {
        cin >> v[i];
        sum += v[i];
    } 

    double mean = (double)sum / n;

    vector <double> v1(n), v2(n);
    double sum1 = 0;

    for(int i = 0; i < n; i++)
    {
        v1[i] = v[i] - mean;
        v2[i] = v1[i]*v1[i];

        sum1 += v2[i];
    }

    double variance = sum1 / (double) n;

    double s_devi = sqrt(variance);

    for(int i = 0; i < n; i++)
    {
        ans[i] = (v[i] - mean) / s_devi;
    }

    cout << "------Z SCORE-----\n\n";
    cout << "MEAN - " << mean << endl;
    cout << "Standard Deviation "<< s_devi << endl;

    cout << "X\t\tX-mean\t\t(X-mean)^2\t\tZ-score\n\n";

    for(int i = 0; i < n; i++)
    {
        cout << v[i] << "\t\t" << v1[i] << "\t\t" << v2[i] << "\t\t" << ans[i] << endl;
    }


    cout << "------MIN MAX-----\n\n";

    int mini = *min_element(begin(v), end(v));
    int maxi = *max_element(begin(v), end(v));

    cout << "MINI - " << mini << endl;
    cout << "MAXI - " << maxi << endl;

    cout << "X\t\tX-min/max-min\n\n";

    for(int i = 0; i < n; i++)
    {
        string str = "";
        str += to_string(v[i]);
        str += " - ";
        str += to_string(mini);
        str += " / ";
        str += to_string(maxi);
        str += " - ";
        str += to_string(mini);

        cout << v[i] << "\t\t" << str << " ----------->  " << (v[i] - mini) / (maxi - mini) << endl;;
    }




}