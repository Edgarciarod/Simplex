#include <iostream>
#include <vector>
#include <cmath>
#include <cfloat>
#include <cstdio>

#define M 10000000

using namespace std;

struct vec
{
  double val;
  int des;
};

struct luz
{
    double value;
    int colom;
    int filan;
};

struct Resultado
{
    vector<double> vec;
    bool sol;
};

Resultado SimpleX(vector< vector<double> > A, vector<vec> B, vector<double> Z);

void pFobjetivo(vector<double> &Z, int numv);
void pFrestric(vector< vector<double> > &A, vector<vec> &B, int numc, int numv);

void cSimplex(vector< vector<double> > &cSim, vector< vector<double> > A, vector<vec> B, vector<double> Z, int numv, int numr, int numa);
void granM(vector< vector<double> > &cSim, int numv, int numr, int columnas, int &fil, int &col, double &val, int i);
bool pivoteM(vector< vector<double> > cSim, int numv, int numr, int columnas, int &fil, int &col, double &val);
void opeSimplex(vector< vector<double> > &cSim, vector<bool> &vSim, luz &valid, int numv, int numr, int numa, int columnas, int &fil, int &col, double &val);
bool pivote(vector< vector<double> > cSim, vector<bool> &vSim, int numv, int numr, int numa, int columnas, int &fil, int &col, double &val);
bool optimal(vector< vector<double> > A, vector<vec> B, vector<double> resultado);

void print(vector< vector<double> > cuadro, int numv, int numc, int columnas, int numa)
{
    cout<<endl<<endl;
    for(int i=0; i<=numc; i++)
    {
        for(int j=0; j<=columnas; j++)
            cout<<cuadro[i][j]<<"\t";
        cout<<endl;
    }
}

int main()
{
    freopen("../data/Entrada.in","r",stdin);
    freopen("../data/Salida.out","w",stdout);
    int numv=2, numr=1;

    cin>>numv>>numr;

    vector<double> Z (numv);
    //, Bb(numc);
    vector<vec> B(numr);
    //vector< vector<double> > B(numc, vector<double> (3,0));
    vector< vector<double> > A(numr, vector<double> (numv,0));
    pFobjetivo(Z, numv);
    pFrestric(A, B, numr, numv);

    Resultado caca;
    caca=SimpleX(A, B, Z);
    for(int i=0; i<numv+1; i++)
        cout<<caca.vec[i]<<" ";
    return 0;
}


void pFobjetivo(vector<double> &Z, int numv)
{
    double var;
    for(int i=0; i<numv; i++)
    {
        //cout<<"Coeficiente en Z para x"<<i+1<<endl;
        cin>>var;
        Z[i]=var;
    }
}

void pFrestric(vector< vector<double> > &A, vector<vec> &B, int numc, int numv)
{
    for(int i=0; i<numc; i++)
    {
        for(int j=0; j<numv+1; j++)
        {
            if(j<numv)
            {
                //cout<<"Coeficiente de X"<<j+1<<" en la restriccion "<<i+1<<endl;
                cin>>A[i][j];
            }
            else
            {
                //cout<<"Valor de B en la restriccion "<<i+1<<endl;
                cin>>B[i].des;
                cin>>B[i].val;
            }
        }
    }
}

Resultado SimpleX(vector< vector<double> > A, vector<vec> B, vector<double> Z)
{
    int numv, numr, numa=0, columnas;
    int fil0, fil, col0, col;
    double val0, val;
    luz valid;

    numv=Z.size();
    numr=B.size();
    columnas=numr;
    for(int i=0; i<numr; i++)
    {
        if(B[i].des==0)
        {
            columnas--;
            numa++;
        }
        else if(B[i].des==1)
            numa++;
    }

    columnas=columnas+numv+numa;
    valid.value=-100000*numa;
    valid.colom=0;

    vector< vector<double> > cSim(numr+1, vector<double> (columnas+1,0));
    vector<bool> vSim;
    vSim.assign(numr,false);

    cSimplex(cSim, A, B, Z, numv, numr, numa);

    if(numa!=0)
        for(int i=0; i<numa; i++)
            granM(cSim, numv, numr, columnas, fil, col, val, i);

    opeSimplex(cSim, vSim, valid, numv, numr, numa, columnas, fil, col, val);

    Resultado result;
    result.vec.assign(numv+1,0);
    result.vec[0]=cSim[numr][columnas];
    for(int i=0; i<numr; i++)
        for(int j=0; j<numv; j++)
            if(cSim[i][j]==1)
                result.vec[j+1]=cSim[i][columnas];
    result.sol=optimal(A, B, result.vec);
    return result;
}

void cSimplex(vector< vector<double> > &cSim, vector< vector<double> > A, vector<vec> B, vector<double> Z, int numv, int numr, int numa)
{
    int hga=numv;
    for(int i=0; i<numr; i++)
        for(int j=0; j<numv; j++)
            cSim[i][j]=A[i][j];

    for(int i=0; i<numr; i++)
    {
        if(B[i].des==1)
            cSim[i][hga]=-1;
        else if(B[i].des==-1)
            cSim[i][hga]=1;
        else
            hga--;
        hga++;
    }

    if(numa>0)
        for(int i=0; i<numr; i++)
        {
            if(B[i].des==0 || B[i].des==1)
            {
                cSim[i][hga]=1;
                cSim[numr][hga]=M;
            }
            else
                hga--;
            hga++;
        }

    for(int i=0; i<numr; i++)
        cSim[i][hga]=B[i].val;
    for(int i=0; i<numv; i++)
        cSim[numr][i]=Z[i]*-1;
}

void granM(vector< vector<double> > &cSim, int numv, int numr, int columnas, int &fil, int &col, double &val, int i)
{
    if(pivoteM(cSim, numv, numr, columnas-i, fil, col, val)==true)
    {
        for(int j=0; j<=columnas; j++)
            cSim[numr][j]=cSim[numr][j]-val*cSim[fil][j];
    }
}

bool pivoteM(vector< vector<double> > cSim, int numv, int numr, int columnas, int &fil, int &col, double &val)
{
    val=0;
    for(int i=numv; i<columnas; i++)
        if(cSim[numr][i]>=val)
        {
            val=cSim[numr][i];
            col=i;
        }
    if(val>0)
    {
        for(int i=0; i<numr; i++)
            if(cSim[i][col]==1)
                fil=i;
        return true;
    }
    return false;
}

void opeSimplex(vector< vector<double> > &cSim, vector<bool> &vSim, luz &valid, int numv, int numr, int numa, int columnas, int &fil, int &col, double &val)
{
    double vs;

    if(pivote(cSim, vSim, numv, numr, numa, columnas, fil, col, val)==true)
    {
        for(int i=0; i<=columnas; i++)
            cSim[fil][i]=cSim[fil][i]/val;

        for(int i=0; i<=numr; i++)
        {
            vs=cSim[i][col];
            if(i!=fil)
                for(int j=0; j<=columnas; j++)
                    cSim[i][j]=cSim[i][j]-vs*cSim[fil][j];
        }
        if(cSim[numr][columnas]<valid.value && pivote(cSim, vSim, numv, numr, numa, columnas, fil, col, val)==true)
        {
            for(int i=0; i<=columnas; i++)
            cSim[fil][i]=cSim[fil][i]/val;

            for(int i=0; i<=numr; i++)
            {
                vs=cSim[i][col];
                if(i!=fil)
                    for(int j=0; j<=columnas; j++)
                        cSim[i][j]=cSim[i][j]-vs*cSim[fil][j];
            }
            vSim[valid.filan]=true;
        }
        else if(col!=valid.colom)
            vSim.assign(numr,false);


        valid.value=cSim[numr][columnas];
        valid.colom=col;
        valid.filan=fil;

        opeSimplex(cSim, vSim, valid, numv, numr, numa, columnas, fil, col, val);
    }
}

bool pivote(vector< vector<double> > cSim, vector<bool> &vSim, int numv, int numr, int numa, int columnas, int &fil, int &col, double &val)
{
    val=0;
    for(int i=0; i<columnas-numa; i++)
        if(cSim[numr][i]<val)
        {
            val=cSim[numr][i];
            col=i;
        }

    if(val<0)
    {
        if(!vSim[0])
        {
            fil=0;
            val=fabs(cSim[0][columnas]/cSim[0][col]);
        }
        else
            val=M;
        for(int i=1; i<numr; i++)
        {
            if(fabs(cSim[i][columnas]/cSim[i][col])<val && !vSim[i])
            {
                val=cSim[i][columnas]/cSim[i][col];
                fil=i;
            }
        }
        val=cSim[fil][col];
        //vSim[fil]=true;

        return true;
    }
    return false;
}

bool optimal(vector< vector<double> > A, vector<vec> B, vector<double> resultado)
{
    int numv,numr;
    double sum;

    numv=A[0].size();
    numr=B.size();
    for(int i=0; i<numr; i++)
    {
        sum=0;
        for(int j=0; j<numv; j++)
            sum+=A[i][j]*resultado[j+1];

        if(B[i].des==0)
            {
                if(fabs(sum)-fabs(B[i].val)>DBL_EPSILON)
                    return false;
            }
        else if(B[i].des>0)
            {
                if(sum<B[i].val || fabs(sum)-fabs(B[i].val)>DBL_EPSILON)
                    return false;
            }

        else if(sum>B[i].val || fabs(sum)-fabs(B[i].val)>DBL_EPSILON)
            return false;
    }
    return true;
}
