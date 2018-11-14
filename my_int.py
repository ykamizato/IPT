
# coding: utf-8

# In[1]:


# このファイルの内容を別のところでモジュールとして使うために.pythonファイルに変換したファイルを作成。

import subprocess
subprocess.run(['jupyter', 'nbconvert', '--to', 'python', '数値積分.ipynb']) 
subprocess.run(['mv', '数値積分.py', 'my_int.py'])                           # 「my_int.py」にリネーム。


# # 数値積分
# 
# 
# 数値積分の説明ために次の1～3次関数
# $$\begin{eqnarray}
# y_a &=& x    \\
# y_b &=& x^2  \\ 
# y_c &=& x^3  \\
# \end{eqnarray}$$
# 
# のそれぞれの積分範囲 $x=-1\to x=1$ の積分
# 
# $$\begin{eqnarray}
# \int_{-1}^{1}y_adx &=& 0  \\ 
# \int_{-1}^{1}y_bdx &=& 2/3 &=& 0.66666...  \\
# \int_{-1}^{1}y_cdx &=& 0  \\
# \end{eqnarray}$$
# 
# を例として今後用いる。  
# 上で行った積分は厳密値であり、これらを今後の数値計算の結果と比較する。
# 

# In[2]:


y_a = lambda x : x
y_b = lambda x : x**2
y_c = lambda x : x**3
x_0 = -1        # 積分の下端
x_n = 1        # 積分の上端


# ## 区分求積法
# 一般に、定積分について、次のような関係が成立すると考えられる。
# 
# $$\int_{x_0}^{x_n}f(x)dx = \lim_{n\to\infty}\sum_{k=1}^{n}f(x_k)\Delta x_{k}$$
# 
# ただし、$x_k$とは積分範囲$x_0\sim x_n$をn等分した分点であり、$\Delta x_k\equiv x_i-x_{i-1}=(x_n-x_0)/n$ である。  
# これを区分求積法という。  
# nを無限大とせず、有限の値で打ち切った場合は、  
# $$\begin{equation}
# \int_{x_0}^{x_n}f(x)dx \simeq \sum_{k=1}^{n}f(x_k)\Delta x_{k}
# \tag{1}
# \end{equation}$$
# が得られる。  
# これは、面積を、有限の幅の長方形を並べたもので近似したということである。  
# (1)式を使って積分を実装したものが以下。

# In[3]:


def int_quad(func,a,b,n) :   
    '''int_quad(func,a,b,n)
        渡された関数funcを区分求積で数値積分した結果を返す。
        a,bはそれぞれ積分の下端と上端。nは分割数。
    '''
    dx = (b-a)/n   # 刻み幅
    result = 0
    x = lambda i : a+dx*i 
    for i in range(1,n+1) :
        result += dx*func(x(i))
    return result

print('y_aの積分誤差', int_quad(y_a,x_0,x_n,100) - 0 )
print('y_bの積分誤差', int_quad(y_b,x_0,x_n,100) - 2/3 )
print('y_cの積分誤差', int_quad(y_c,x_0,x_n,100) - 0 )


# ## 台形則
# $f_{line}(x)$を1次関数とする。$f_{line}(x)$の定積分を行うことは台形面積を計算することであるから
# 
# $$\begin{equation}
# \int_{a}^{b}f_{line}(x)dx = (b-a)\frac{f_{line}(a)+f_{line}(b)}{2}
# \tag{2}
# \end{equation}$$
# 
# が厳密に成り立つ。  
# 一般の関数$f(x)$の定積分についても、積分範囲をn等分し、それぞれの区間でf(x)を1次関数に近似して上の関係を用いれば  
# 
# $$\begin{eqnarray}
# \int_{x_0}^{x_n}f(x)dx &\simeq& \sum_{i=1}^{n}(x_i-x_{i-1})\frac{f(x_{i-1})+f(x_i)}{2}  \\
# &=& \frac{x_n-x_0}{n}\sum_{i=1}^{n}\frac{f(x_{i-1})+f(x_i)}{2} \\
# &=& \Delta x_k\sum_{i=1}^{n}\frac{f(x_{i-1})+f(x_i)}{2}
# \tag{3}
# \end{eqnarray}$$ 
# 
# という近似式が得られる。これを台形則という。  
# 区分求積では長方形を並べて面積を近似したのに対し、(3)は台形を並べて近似している。  
# $n\to\infty$では、この関係は$\simeq$でなく$=$の厳密式になる。 
# 
# プラグラムに実装するには(3)式で十分だが、(3)式をちょっと変形すると
# 
# $$\begin{eqnarray}
# \Delta x_k\sum_{i=1}^{n}\frac{f(x_{i-1})+f(x_i)}{2} &=& \frac{\Delta x_k}{2}f(x_0)+\sum_{k=1}^{n-1}\Delta x_kf(x_k)+\frac{\Delta x_k}{2}f(x_n) \\
# &=& \frac{\Delta x_k}{2}f(x_0)+\sum_{k=1}^{n}\Delta x_kf(x_k)-\frac{\Delta x_k}{2}f(x_n)
# \tag{4}
# \end{eqnarray}$$
#  
# が得られ、この最右辺のΣの項は区分求積と同じ形であることが分かる。ゆえに、結局のところ台形則とは、区分求積に対して
# 
# $$\begin{equation}
# \frac{\Delta x_k}{2}(f(x_0)-f(x_n))
# \tag{5}
# \end{equation}$$
# 
# という、両端についての補正項を加えたものだと言える。これは幾何学的には、台形から長方形を差っ引いてできる三角形の面積の合計になっている。(簡単な計算で分かる)  
# (4)式を用いて$y_1(x),y_2(x),y_3(x)$を数値積分したものが以下。（区分求積を使いまわせばいいので一瞬で終わる）

# In[4]:


def int_trapz(func,a,b,n) : 
    '''int_trapz(func,a,b,n)
        渡された関数funcを台形則で数値積分した結果を返す。
        a,bはそれぞれ積分の下端と上端。nは分割数。
    '''
    dx = (b-a)/n   # 刻み幅
    return int_quad(func,a,b,n) + (dx/2)*(func(a)-func(b))  # 区分求積に補正項を加算

print('y_aの積分誤差', int_trapz(y_a,x_0,x_n,100) - 0 )
print('y_bの積分誤差', int_trapz(y_b,x_0,x_n,100) - 2/3 )
print('y_cの積分誤差', int_trapz(y_c,x_0,x_n,100) - 0 )


# 明らかに精度が上がっていることが分かる。  
# 特に、$y_a = x$ の誤差が著しく減っているが、これは台形則がf(x)を区分ごとに1次関数に近似して積分を実行する方法であるために、そもそも1次関数に対しては近似でなく厳密な計算になるからである。（ごくわずかな誤差が生じているのは別の原因かと思われる。）  
# しかし一方で、2次関数 $y_b = x^2$ については誤差が区分求積のときと全く変わっていない。これは、
# $$f(x_0)=f(x_n)$$
# を満たすとき、補正項(5)式がゼロとなるからである。  
# このように、積分範囲の両端で被積分関数の値が一致する場合は区分求積と台形則は全く同じになる。そうでなくとも、両端の寄与が小さい場合は、区分求積と台形則の結果はあまり変わらない。
# 
# 
# scipyには台形則による数値積分を行ってくれる関数trapz()があるのでそれを用いることもできる。
# 

# In[5]:


import numpy as np
from scipy import integrate

n=100  # 分割数
x = np.linspace(x_0, x_n, n)
y_a_array = x
y_b_array = x**2
y_c_array = x**3

print('y_1の積分誤差：', integrate.trapz(y_a_array,x) - 0)
print('y_2の積分誤差：', integrate.trapz(y_b_array,x) -2/3)
print('y_3の積分誤差：', integrate.trapz(y_c_array,x) - 0)


# （なぜか結果が微妙に異なる。）

# ### 補足：シンプソン則
# 
# 2次関数の定積分についても(1)式のような厳密な関係式が存在し、シンプソンの公式と呼ばれる。(さらに高次のものも一般に存在することが示せる)  
# 台形則の場合と同様に、各区間を2次で近似してシンプソン公式により数値積分を行うこともできる。  
# scipyのsimps関数を使って計算でき

# In[6]:


print('y_aの積分誤差：', integrate.simps(y_a_array,x) - 0)
print('y_bの積分誤差：', integrate.simps(y_b_array,x) - 2/3)
print('y_cの積分誤差：', integrate.simps(y_c_array,x) - 0)


# 
# 
# 

# ## 誤差
# 
# 台形則を用いた積分近似(2)式の誤差はおよそ
# 
# $$\begin{equation}
# -\frac{(b-a)^2}{12n^2}[f'(b)-f'(a)]+O(\frac{1}{n^4})
# \tag{3}
# \end{equation}$$
# 
# と、$1/n^2$のオーダーになる。  
# シンプソンの場合は
# 
# $$-\frac{(b-a)^4}{180n^4}[f'''(b)-f'''(a)]+O(\frac{1}{n^5})$$
# 
# と、$1/n^4$のオーダーになる。  
# このように高次の近似ほど精度が良くなるが、積分範囲が $-\infty～\infty$ の場合においては例外的に台形則が良い結果を与えるらしい。(無限個の和をとることはできないので、和の範囲はどこかで打ち切る)
# 
# 

# ## 2重指数関数型積分（DE）
# 
# 台形則を用いて数値積分を行う場合、(3)式より、積分範囲の両端の傾き$f'(a) , f'(b)$の差が大きいと誤差が大きくなってしまう。  
# ゆえに、$f'(x)$が積分の端で特異性を持つような場合などではそのまま台形則を使うのはまずそう。  
# そこで積分に変数変換を施して、特異性の無い形に直してから台形則を適用することを行う。  
# 例えば、積分範囲が-1～1の積分
# 
# $$S = \int_{-1}^{1}f(x)dx$$
# 
# に対しては $x = \phi(t) = \tanh(\frac{\pi}{2}\sinh(t))$ と変換して
# 
# $$S = \int_{-\infty}^{\infty}f(\phi(t))\phi'(t)dt$$
# 
# とした場合、この被積分関数は $t\to\pm\infty$で
# 
# $$ f(\phi(t))\phi'(t) \sim \exp\{-c\exp(-|t|)\} \to 0 $$
# 
# と、指数の肩に指数という急速な減衰をする。この急速な減衰が特異性を無くす。  
# きざみ幅 $h$ の台形則を適用して  
# 
# $$\begin{eqnarray}
# S &\simeq& h\sum_{k=-\infty}^{\infty}f(\phi(kh))\phi'(kh) \\
# &=& \frac{\pi}{2}h\sum_{k=-\infty}^{\infty}f(\tanh(\frac{\pi}{2}\sinh{kh}))\frac{\cosh(kh)}{\cosh^{2}(\frac{\pi}{2}\sinh(kh))} \\
# \tag{4}
# \end{eqnarray}$$
# 
# となる。  
# 台形則を適用して離散化したところだけでなく(4)式の無限和の打ち切りでも誤差が生じる。
# 

# In[7]:


def int_DE(func,a,b,n,N) :
    '''int_DE(func,a,b,n,N)
        渡された関数funcを2重指数関数型積分した結果を返す。
        a,bはそれぞれ積分の下端と上端。nは分割数。和の範囲は第N項で打ち切る。
    '''
    result= 0
    dx = (b-a)/n    # 刻み幅
    for i in range(-N,N+1) :
        sh = np.pi/2*np.sinh(i*dx)
        result += np.pi/2*dx*func(np.tanh(sh))*np.cosh(i*dx)/(np.cosh(sh)**2)     
    return result

print('y_aの積分誤差：', int_DE(y_a,x_0,x_n,100,1000) - 0)
print('y_bの積分誤差：', int_DE(y_b,x_0,x_n,100,1000) - 2/3)
print('y_cの積分誤差：', int_DE(y_c,x_0,x_n,100,1000) - 0)


# ### ガウス・ルジャンドル積分

# In[8]:


def int_gauss(func,a,b,n) :
    '''int_gauss(func,a,b,n)
        渡された関数funcをガウス・ルジャンドル積分した結果を返す。
        a,bはそれぞれ積分の下端と上端。nは分割数。
    '''
    x, w = np.polynomial.legendre.leggauss(n)
    return (b-a)/2*sum( w * func((b-a)/2*x + (b+a)/2) )

print('y_1の積分誤差：', int_gauss(y_a,x_0,x_n,100) - 0)
print('y_2の積分誤差：', int_gauss(y_b,x_0,x_n,100) - 2/3)
print('y_3の積分誤差：', int_gauss(y_c,x_0,x_n,100) - 0)

