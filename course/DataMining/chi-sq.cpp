#include <bits/stdc++.h>
using namespace std;


int main()
{
    int n, m;
    cout << "ENTER THEE ROW AND COL : ";
    cin >> n >> m;

    vector <vector <double>> arr(n+1, vector <double> (m+1, 0));
    vector <vector <double>> temp(n+1, vector <double> (m+1, 0));

    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < m; j++)
        {
            cin >> arr[i][j];
        }
    }

    std::cout << std::setprecision(2) << std::fixed;

    cout << "-----CHI SQ-----\n\n";
    
    for(int i = 0; i < n; i++)
    {
        double sum = 0;
        for(int j = 0; j < m; j++)
        {
            cout << arr[i][j] << "\t";
            sum += arr[i][j];
        }

        arr[i][m] = sum;
        cout << arr[i][m] << "\t";

        cout << endl;
    }

    double g_total = 0;
    for(int j = 0; j < m; j++)
    {
        double sum = 0;
        for(int i = 0; i < n; i++)
        {
            sum += arr[i][j];
        }

        arr[n][j] = sum;
        cout << arr[n][j] << "\t";

        g_total += sum;
    }

    cout << g_total << endl;

    cout << "\n\n";

    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
        {
            temp[i][j] = arr[i][m] * arr[n][j] / g_total;
            cout << temp[i][j] << "\t";
        }

        cout << endl;
    }

    cout << "\n\nOBSERVE\t\tEXPECTED\t\t(O_E)^2 / E \n\n";

    double sum = 0;

    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
        {
            sum += (temp[i][i] - arr[i][i])*(temp[i][i] - arr[i][i]) / temp[i][j];
            cout << arr[i][j] << "\t\t" << temp[i][i] << "\t\t" << (temp[i][i] - arr[i][i])*(temp[i][i] - arr[i][i]) / temp[i][j] << endl;
        }
    }

    cout << "\n\n Chi sq TABULAR ----->> SEE FROM TABLE" << endl;
    cout << "\n\n Chi sq CALCULATED ----->> " << sum;


}