# 独立校检逐条清单

这里同时列出独立物理校检和辅助数值检查；辅助项不能单独证明哈密顿量正确。

期望值与实测值的绝对差不超过所列容差即通过。错误类型与其对应的失败方式详见 result.md 的校检策略。

| 编号 | 校检 | 针对的错误类型 | 期望值 | 实测值 | 容差 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | two-site analytic full spectrum | spin factor and sign | 0 | 0 | 1e-14 | 通过 |
| 2 | ED Hermitian N=4 J2=0.0 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 3 | ED residual N=4 J2=0.0 P=False | eigensolver convergence (auxiliary) | 0 | 3.33066907388e-16 | 2e-08 | 通过 |
| 4 | ED tensor action N=4 J2=0.0 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 2.71947991102e-16 | 1e-11 | 通过 |
| 5 | untruncated N=4 J2=0.0 | missing or duplicated cross-boundary bonds | -1.61602540378 | -1.61602540378 | 2e-10 | 通过 |
| 6 | untruncated physical residual N=4 J2=0.0 | edge positions and tensor order | 0 | 3.59753377e-16 | 2e-09 | 通过 |
| 7 | ED Hermitian N=6 J2=0.0 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 8 | ED residual N=6 J2=0.0 P=False | eigensolver convergence (auxiliary) | 0 | 6.12600593149e-16 | 2e-08 | 通过 |
| 9 | ED tensor action N=6 J2=0.0 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 3.38817741194e-16 | 1e-11 | 通过 |
| 10 | untruncated N=6 J2=0.0 | missing or duplicated cross-boundary bonds | -2.49357713389 | -2.49357713389 | 2e-10 | 通过 |
| 11 | untruncated physical residual N=6 J2=0.0 | edge positions and tensor order | 0 | 1.12419718183e-15 | 2e-09 | 通过 |
| 12 | ED Hermitian N=8 J2=0.0 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 13 | ED residual N=8 J2=0.0 P=False | eigensolver convergence (auxiliary) | 0 | 8.63302262064e-16 | 2e-08 | 通过 |
| 14 | ED tensor action N=8 J2=0.0 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 5.86952750816e-16 | 1e-11 | 通过 |
| 15 | untruncated N=8 J2=0.0 | missing or duplicated cross-boundary bonds | -3.37493259869 | -3.37493259869 | 2e-10 | 通过 |
| 16 | untruncated physical residual N=8 J2=0.0 | edge positions and tensor order | 0 | 2.12246763022e-15 | 2e-09 | 通过 |
| 17 | ED Hermitian N=10 J2=0.0 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 18 | ED residual N=10 J2=0.0 P=False | eigensolver convergence (auxiliary) | 0 | 1.45426897107e-12 | 2e-08 | 通过 |
| 19 | untruncated N=10 J2=0.0 | missing or duplicated cross-boundary bonds | -4.25803520728 | -4.25803520728 | 2e-10 | 通过 |
| 20 | untruncated physical residual N=10 J2=0.0 | edge positions and tensor order | 0 | 2.15133326951e-12 | 2e-09 | 通过 |
| 21 | ED Hermitian N=4 J2=0.3 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 22 | ED residual N=4 J2=0.3 P=False | eigensolver convergence (auxiliary) | 0 | 9.67272850329e-16 | 2e-08 | 通过 |
| 23 | ED tensor action N=4 J2=0.3 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 1.67685948094e-16 | 1e-11 | 通过 |
| 24 | untruncated N=4 J2=0.3 | missing or duplicated cross-boundary bonds | -1.52449979984 | -1.52449979984 | 2e-10 | 通过 |
| 25 | untruncated physical residual N=4 J2=0.3 | edge positions and tensor order | 0 | 1.14741697302e-15 | 2e-09 | 通过 |
| 26 | ED Hermitian N=6 J2=0.3 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 27 | ED residual N=6 J2=0.3 P=False | eigensolver convergence (auxiliary) | 0 | 9.80929373565e-16 | 2e-08 | 通过 |
| 28 | ED tensor action N=6 J2=0.3 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 4.11690852789e-16 | 1e-11 | 通过 |
| 29 | untruncated N=6 J2=0.3 | missing or duplicated cross-boundary bonds | -2.30477549532 | -2.30477549532 | 2e-10 | 通过 |
| 30 | untruncated physical residual N=6 J2=0.3 | edge positions and tensor order | 0 | 1.92391469909e-15 | 2e-09 | 通过 |
| 31 | ED Hermitian N=8 J2=0.3 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 32 | ED residual N=8 J2=0.3 P=False | eigensolver convergence (auxiliary) | 0 | 1.25873236904e-15 | 2e-08 | 通过 |
| 33 | ED tensor action N=8 J2=0.3 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 9.93062455706e-16 | 1e-11 | 通过 |
| 34 | untruncated N=8 J2=0.3 | missing or duplicated cross-boundary bonds | -3.08744625787 | -3.08744625787 | 2e-10 | 通过 |
| 35 | untruncated physical residual N=8 J2=0.3 | edge positions and tensor order | 0 | 1.26049793029e-14 | 2e-09 | 通过 |
| 36 | ED Hermitian N=10 J2=0.3 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 37 | ED residual N=10 J2=0.3 P=False | eigensolver convergence (auxiliary) | 0 | 3.58829340864e-15 | 2e-08 | 通过 |
| 38 | untruncated N=10 J2=0.3 | missing or duplicated cross-boundary bonds | -3.87130470748 | -3.87130470748 | 2e-10 | 通过 |
| 39 | untruncated physical residual N=10 J2=0.3 | edge positions and tensor order | 0 | 4.12819742261e-15 | 2e-09 | 通过 |
| 40 | ED Hermitian N=4 J2=0.5 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 41 | ED residual N=4 J2=0.5 P=False | eigensolver convergence (auxiliary) | 0 | 1.05407313433e-15 | 2e-08 | 通过 |
| 42 | ED tensor action N=4 J2=0.5 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 2.89847607742e-17 | 1e-11 | 通过 |
| 43 | untruncated N=4 J2=0.5 | missing or duplicated cross-boundary bonds | -1.5 | -1.5 | 2e-10 | 通过 |
| 44 | untruncated physical residual N=4 J2=0.5 | edge positions and tensor order | 0 | 1.08584267367e-15 | 2e-09 | 通过 |
| 45 | ED Hermitian N=6 J2=0.5 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 46 | ED residual N=6 J2=0.5 P=False | eigensolver convergence (auxiliary) | 0 | 1.39234749542e-15 | 2e-08 | 通过 |
| 47 | ED tensor action N=6 J2=0.5 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 3.40493896515e-16 | 1e-11 | 通过 |
| 48 | untruncated N=6 J2=0.5 | missing or duplicated cross-boundary bonds | -2.25 | -2.25 | 2e-10 | 通过 |
| 49 | untruncated physical residual N=6 J2=0.5 | edge positions and tensor order | 0 | 1.83243026583e-15 | 2e-09 | 通过 |
| 50 | ED Hermitian N=8 J2=0.5 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 51 | ED residual N=8 J2=0.5 P=False | eigensolver convergence (auxiliary) | 0 | 1.85753476844e-15 | 2e-08 | 通过 |
| 52 | ED tensor action N=8 J2=0.5 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 4.86566808836e-16 | 1e-11 | 通过 |
| 53 | untruncated N=8 J2=0.5 | missing or duplicated cross-boundary bonds | -3 | -3 | 2e-10 | 通过 |
| 54 | untruncated physical residual N=8 J2=0.5 | edge positions and tensor order | 0 | 3.20085939277e-13 | 2e-09 | 通过 |
| 55 | ED Hermitian N=10 J2=0.5 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 56 | ED residual N=10 J2=0.5 P=False | eigensolver convergence (auxiliary) | 0 | 4.52910659069e-15 | 2e-08 | 通过 |
| 57 | untruncated N=10 J2=0.5 | missing or duplicated cross-boundary bonds | -3.75 | -3.75 | 2e-10 | 通过 |
| 58 | untruncated physical residual N=10 J2=0.5 | edge positions and tensor order | 0 | 8.73196727219e-15 | 2e-09 | 通过 |
| 59 | ED Hermitian N=4 J2=0.0 P=True | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 60 | ED residual N=4 J2=0.0 P=True | eigensolver convergence (auxiliary) | 0 | 1.72352961861e-15 | 2e-08 | 通过 |
| 61 | ED tensor action N=4 J2=0.0 P=True | wrong bonds, spin normalization, transverse sign, boundary | 0 | 0 | 1e-11 | 通过 |
| 62 | ED Hermitian N=6 J2=0.0 P=True | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 63 | ED residual N=6 J2=0.0 P=True | eigensolver convergence (auxiliary) | 0 | 1.1140328793e-15 | 2e-08 | 通过 |
| 64 | ED tensor action N=6 J2=0.0 P=True | wrong bonds, spin normalization, transverse sign, boundary | 0 | 2.55893763326e-16 | 1e-11 | 通过 |
| 65 | ED Hermitian N=8 J2=0.0 P=True | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 66 | ED residual N=8 J2=0.0 P=True | eigensolver convergence (auxiliary) | 0 | 1.37626886513e-15 | 2e-08 | 通过 |
| 67 | ED tensor action N=8 J2=0.0 P=True | wrong bonds, spin normalization, transverse sign, boundary | 0 | 4.22831507991e-16 | 1e-11 | 通过 |
| 68 | ED Hermitian N=12 J2=0.0 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 69 | ED residual N=12 J2=0.0 P=False | eigensolver convergence (auxiliary) | 0 | 1.78497622626e-15 | 2e-08 | 通过 |
| 70 | projection m=2 dm | energy evaluated with wrong H or tensor ordering | 0 | 0 | 2e-10 | 通过 |
| 71 | projection m=2 energy | energy evaluated with wrong H or tensor ordering | 0 | 8.881784197e-16 | 2e-10 | 通过 |
| 72 | discard norm m=2 | wrong Schmidt weight sum | 0.0880141739777 | 0.0880141739777 | 2e-12 | 通过 |
| 73 | projection m=4 dm | energy evaluated with wrong H or tensor ordering | 0 | 1.7763568394e-15 | 2e-10 | 通过 |
| 74 | projection m=4 energy | energy evaluated with wrong H or tensor ordering | 0 | 0 | 2e-10 | 通过 |
| 75 | discard norm m=4 | wrong Schmidt weight sum | 0.000261974889811 | 0.000261974889811 | 2e-12 | 通过 |
| 76 | projection m=6 dm | energy evaluated with wrong H or tensor ordering | 0 | 1.7763568394e-15 | 2e-10 | 通过 |
| 77 | projection m=6 energy | energy evaluated with wrong H or tensor ordering | 0 | 1.7763568394e-15 | 2e-10 | 通过 |
| 78 | discard norm m=6 | wrong Schmidt weight sum | 0.00010650455411 | 0.00010650455411 | 2e-12 | 通过 |
| 79 | projection m=8 dm | energy evaluated with wrong H or tensor ordering | 0 | 0 | 2e-10 | 通过 |
| 80 | projection m=8 energy | energy evaluated with wrong H or tensor ordering | 0 | 0 | 2e-10 | 通过 |
| 81 | discard norm m=8 | wrong Schmidt weight sum | 4.9912488443e-06 | 4.99124884401e-06 | 2e-12 | 通过 |
| 82 | projection m=12 dm | energy evaluated with wrong H or tensor ordering | 0 | 1.7763568394e-15 | 2e-10 | 通过 |
| 83 | projection m=12 energy | energy evaluated with wrong H or tensor ordering | 0 | 8.881784197e-16 | 2e-10 | 通过 |
| 84 | discard norm m=12 | wrong Schmidt weight sum | 8.75479281915e-07 | 8.75479281515e-07 | 2e-12 | 通过 |
| 85 | projection m=16 dm | energy evaluated with wrong H or tensor ordering | 0 | 0 | 2e-10 | 通过 |
| 86 | projection m=16 energy | energy evaluated with wrong H or tensor ordering | 0 | 1.7763568394e-15 | 2e-10 | 通过 |
| 87 | discard norm m=16 | wrong Schmidt weight sum | 1.60605512734e-08 | 1.60605510002e-08 | 2e-12 | 通过 |
| 88 | MG energy N=8 | J2 coefficient, OBC, spin factor | -3 | -3 | 2e-10 | 通过 |
| 89 | MG dimer residual N=8 | wrong J2 or crossing bonds (analytic vector) | 0 | 0 | 2e-12 | 通过 |
| 90 | MG overlap N=8 | wrong ED ground state or bit order | 1 | 1 | 2e-10 | 通过 |
| 91 | MG entropy analytic N=8 | wrong cut or Schmidt coefficients | 0 | 4.4408920985e-16 | 2e-10 | 通过 |
| 92 | MG entropy rho N=8 | entropy algorithm | 0 | 2.22044604925e-16 | 2e-10 | 通过 |
| 93 | MG energy N=10 | J2 coefficient, OBC, spin factor | -3.75 | -3.75 | 2e-10 | 通过 |
| 94 | MG dimer residual N=10 | wrong J2 or crossing bonds (analytic vector) | 0 | 2.71947991102e-16 | 2e-12 | 通过 |
| 95 | MG overlap N=10 | wrong ED ground state or bit order | 1 | 1 | 2e-10 | 通过 |
| 96 | MG entropy analytic N=10 | wrong cut or Schmidt coefficients | 0 | 1.11022302463e-15 | 2e-10 | 通过 |
| 97 | MG entropy rho N=10 | entropy algorithm | 0 | 8.881784197e-16 | 2e-10 | 通过 |
| 98 | ED Hermitian N=12 J2=0.5 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 99 | ED residual N=12 J2=0.5 P=False | eigensolver convergence (auxiliary) | 0 | 4.02699546767e-12 | 2e-08 | 通过 |
| 100 | MG energy N=12 | J2 coefficient, OBC, spin factor | -4.5 | -4.5 | 2e-10 | 通过 |
| 101 | MG dimer residual N=12 | wrong J2 or crossing bonds (analytic vector) | 0 | 5.20740757162e-16 | 2e-12 | 通过 |
| 102 | MG overlap N=12 | wrong ED ground state or bit order | 1 | 1 | 2e-10 | 通过 |
| 103 | MG entropy analytic N=12 | wrong cut or Schmidt coefficients | 0 | 4.4408920985e-16 | 2e-10 | 通过 |
| 104 | MG entropy rho N=12 | entropy algorithm | 0 | 1.11022302463e-15 | 2e-10 | 通过 |
| 105 | ED Hermitian N=14 J2=0.5 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 106 | ED residual N=14 J2=0.5 P=False | eigensolver convergence (auxiliary) | 0 | 1.82922143543e-12 | 2e-08 | 通过 |
| 107 | MG energy N=14 | J2 coefficient, OBC, spin factor | -5.25 | -5.25 | 2e-10 | 通过 |
| 108 | MG dimer residual N=14 | wrong J2 or crossing bonds (analytic vector) | 0 | 4.4408920985e-16 | 2e-12 | 通过 |
| 109 | MG overlap N=14 | wrong ED ground state or bit order | 1 | 1 | 2e-10 | 通过 |
| 110 | MG entropy analytic N=14 | wrong cut or Schmidt coefficients | 0 | 8.881784197e-16 | 2e-10 | 通过 |
| 111 | MG entropy rho N=14 | entropy algorithm | 0 | 9.99200722163e-16 | 2e-10 | 通过 |
| 112 | ED Hermitian N=16 J2=0.5 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 113 | ED residual N=16 J2=0.5 P=False | eigensolver convergence (auxiliary) | 0 | 9.35393291894e-15 | 2e-08 | 通过 |
| 114 | MG energy N=16 | J2 coefficient, OBC, spin factor | -6 | -6 | 2e-10 | 通过 |
| 115 | MG dimer residual N=16 | wrong J2 or crossing bonds (analytic vector) | 0 | 6.91108259398e-16 | 2e-12 | 通过 |
| 116 | MG overlap N=16 | wrong ED ground state or bit order | 1 | 1 | 2e-10 | 通过 |
| 117 | MG entropy analytic N=16 | wrong cut or Schmidt coefficients | 0 | 1.55431223448e-15 | 2e-10 | 通过 |
| 118 | MG entropy rho N=16 | entropy algorithm | 0 | 1.22124532709e-15 | 2e-10 | 通过 |
| 119 | variance tensor J2=0.0 | H differs from independent local tensor contractions | 0 | 9.55895419026e-16 | 2e-11 | 通过 |
| 120 | variance subtract vs norm J2=0.0 | catastrophic cancellation or H squared implementation | 3.18614012831e-30 | -1.7763568394e-14 | 2e-11 | 通过 |
| 121 | variance tensor J2=0.5 | H differs from independent local tensor contractions | 0 | 1.5827715948e-15 | 2e-11 | 通过 |
| 122 | variance subtract vs norm J2=0.5 | catastrophic cancellation or H squared implementation | 1.62166924967e-23 | -1.06581410364e-14 | 2e-11 | 通过 |
| 123 | physical N=4 J2=0.0 chi=2 growth 0 | wrong boundary operators, charge sectors, right-block reversal | -1.61602540378 | -1.61602540378 | 2e-09 | 通过 |
| 124 | physical N=6 J2=0.0 chi=2 growth 1 | wrong boundary operators, charge sectors, right-block reversal | -2.32873030595 | -2.32873030595 | 2e-09 | 通过 |
| 125 | physical N=8 J2=0.0 chi=2 growth 2 | wrong boundary operators, charge sectors, right-block reversal | -3.19711109672 | -3.19711109672 | 2e-09 | 通过 |
| 126 | physical N=10 J2=0.0 chi=2 growth 3 | wrong boundary operators, charge sectors, right-block reversal | -3.94657299608 | -3.94657299608 | 2e-09 | 通过 |
| 127 | physical N=12 J2=0.0 chi=2 growth 4 | wrong boundary operators, charge sectors, right-block reversal | -4.81500618351 | -4.81500618351 | 2e-09 | 通过 |
| 128 | ED Hermitian N=14 J2=0.0 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 129 | ED residual N=14 J2=0.0 P=False | eigensolver convergence (auxiliary) | 0 | 2.37140616812e-13 | 2e-08 | 通过 |
| 130 | physical N=14 J2=0.0 chi=2 growth 5 | wrong boundary operators, charge sectors, right-block reversal | -5.60979057332 | -5.60979057332 | 2e-09 | 通过 |
| 131 | ED Hermitian N=16 J2=0.0 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 132 | ED residual N=16 J2=0.0 P=False | eigensolver convergence (auxiliary) | 0 | 8.56633233135e-15 | 2e-08 | 通过 |
| 133 | physical N=16 J2=0.0 chi=2 growth 6 | wrong boundary operators, charge sectors, right-block reversal | -6.47633423532 | -6.47633423532 | 2e-09 | 通过 |
| 134 | ED Hermitian N=18 J2=0.0 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 135 | ED residual N=18 J2=0.0 P=False | eigensolver convergence (auxiliary) | 0 | 1.0140491798e-13 | 2e-08 | 通过 |
| 136 | physical N=18 J2=0.0 chi=2 growth 7 | wrong boundary operators, charge sectors, right-block reversal | -7.30431891951 | -7.30431891951 | 2e-09 | 通过 |
| 137 | ED Hermitian N=20 J2=0.0 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 138 | ED residual N=20 J2=0.0 P=False | eigensolver convergence (auxiliary) | 0 | 2.35854578253e-14 | 2e-08 | 通过 |
| 139 | ED tensor action N=20 J2=0.0 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 2.59452542033e-15 | 1e-11 | 通过 |
| 140 | physical N=20 J2=0.0 chi=2 growth 8 | wrong boundary operators, charge sectors, right-block reversal | -8.16714899407 | -8.16714899407 | 2e-09 | 通过 |
| 141 | physical N=20 J2=0.0 chi=2 sweep 0 | wrong boundary operators, charge sectors, right-block reversal | -8.32559496939 | -8.32559496939 | 2e-09 | 通过 |
| 142 | physical N=20 J2=0.0 chi=2 sweep 1 | wrong boundary operators, charge sectors, right-block reversal | -8.33013091396 | -8.33013091396 | 2e-09 | 通过 |
| 143 | physical N=20 J2=0.0 chi=2 sweep 2 | wrong boundary operators, charge sectors, right-block reversal | -8.33034847874 | -8.33034847874 | 2e-09 | 通过 |
| 144 | physical N=20 J2=0.0 chi=2 sweep 3 | wrong boundary operators, charge sectors, right-block reversal | -8.33036135831 | -8.33036135831 | 2e-09 | 通过 |
| 145 | physical N=20 J2=0.0 chi=2 sweep 4 | wrong boundary operators, charge sectors, right-block reversal | -8.33036213316 | -8.33036213316 | 2e-09 | 通过 |
| 146 | physical N=20 J2=0.0 chi=2 sweep 5 | wrong boundary operators, charge sectors, right-block reversal | -8.33036217975 | -8.33036217975 | 2e-09 | 通过 |
| 147 | physical N=20 J2=0.0 chi=2 sweep 6 | wrong boundary operators, charge sectors, right-block reversal | -8.33036218254 | -8.33036218254 | 2e-09 | 通过 |
| 148 | physical N=20 J2=0.0 chi=2 sweep 7 | wrong boundary operators, charge sectors, right-block reversal | -8.33036218271 | -8.33036218271 | 2e-09 | 通过 |
| 149 | chi cap J2=0.0 chi=2 | per-sector cap erroneously multiplies total dimension | 0 | 0 | 0 | 通过 |
| 150 | projection loss J2=0.0 chi=2 | discard weight or selected singular vectors | 0 | 1.05210978818e-15 | 2e-12 | 通过 |
| 151 | charge retention J2=0.0 chi=2 | mixing charge sectors in truncation | 0 | 0 | 2e-12 | 通过 |
| 152 | isometry J2=0.0 chi=2 | nonorthogonal projected basis | 0 | 1.33226762955e-15 | 2e-11 | 通过 |
| 153 | local eigensolver J2=0.0 chi=2 | unconverged superblock solver (auxiliary) | 0 | 5.17207855273e-15 | 2e-08 | 通过 |
| 154 | physical N=4 J2=0.0 chi=4 growth 0 | wrong boundary operators, charge sectors, right-block reversal | -1.61602540378 | -1.61602540378 | 2e-09 | 通过 |
| 155 | physical N=6 J2=0.0 chi=4 growth 1 | wrong boundary operators, charge sectors, right-block reversal | -2.49357713389 | -2.49357713389 | 2e-09 | 通过 |
| 156 | physical N=8 J2=0.0 chi=4 growth 2 | wrong boundary operators, charge sectors, right-block reversal | -3.37185512641 | -3.37185512641 | 2e-09 | 通过 |
| 157 | physical N=10 J2=0.0 chi=4 growth 3 | wrong boundary operators, charge sectors, right-block reversal | -4.25403979667 | -4.25403979667 | 2e-09 | 通过 |
| 158 | physical N=12 J2=0.0 chi=4 growth 4 | wrong boundary operators, charge sectors, right-block reversal | -5.13248089353 | -5.13248089353 | 2e-09 | 通过 |
| 159 | physical N=14 J2=0.0 chi=4 growth 5 | wrong boundary operators, charge sectors, right-block reversal | -6.01551380377 | -6.01551380377 | 2e-09 | 通过 |
| 160 | physical N=16 J2=0.0 chi=4 growth 6 | wrong boundary operators, charge sectors, right-block reversal | -6.89361613978 | -6.89361613978 | 2e-09 | 通过 |
| 161 | physical N=18 J2=0.0 chi=4 growth 7 | wrong boundary operators, charge sectors, right-block reversal | -7.77687480383 | -7.77687480383 | 2e-09 | 通过 |
| 162 | physical N=20 J2=0.0 chi=4 growth 8 | wrong boundary operators, charge sectors, right-block reversal | -8.65479766586 | -8.65479766586 | 2e-09 | 通过 |
| 163 | physical N=20 J2=0.0 chi=4 sweep 0 | wrong boundary operators, charge sectors, right-block reversal | -8.65480021605 | -8.65480021605 | 2e-09 | 通过 |
| 164 | physical N=20 J2=0.0 chi=4 sweep 1 | wrong boundary operators, charge sectors, right-block reversal | -8.6548001622 | -8.6548001622 | 2e-09 | 通过 |
| 165 | physical N=20 J2=0.0 chi=4 sweep 2 | wrong boundary operators, charge sectors, right-block reversal | -8.65480016213 | -8.65480016213 | 2e-09 | 通过 |
| 166 | chi cap J2=0.0 chi=4 | per-sector cap erroneously multiplies total dimension | 0 | 0 | 0 | 通过 |
| 167 | projection loss J2=0.0 chi=4 | discard weight or selected singular vectors | 0 | 1.18384035214e-15 | 2e-12 | 通过 |
| 168 | charge retention J2=0.0 chi=4 | mixing charge sectors in truncation | 0 | 0 | 2e-12 | 通过 |
| 169 | isometry J2=0.0 chi=4 | nonorthogonal projected basis | 0 | 1.75773894574e-15 | 2e-11 | 通过 |
| 170 | local eigensolver J2=0.0 chi=4 | unconverged superblock solver (auxiliary) | 0 | 8.20827376325e-15 | 2e-08 | 通过 |
| 171 | physical N=4 J2=0.0 chi=8 growth 0 | wrong boundary operators, charge sectors, right-block reversal | -1.61602540378 | -1.61602540378 | 2e-09 | 通过 |
| 172 | physical N=6 J2=0.0 chi=8 growth 1 | wrong boundary operators, charge sectors, right-block reversal | -2.49357713389 | -2.49357713389 | 2e-09 | 通过 |
| 173 | physical N=8 J2=0.0 chi=8 growth 2 | wrong boundary operators, charge sectors, right-block reversal | -3.37493259869 | -3.37493259869 | 2e-09 | 通过 |
| 174 | physical N=10 J2=0.0 chi=8 growth 3 | wrong boundary operators, charge sectors, right-block reversal | -4.25802248915 | -4.25802248915 | 2e-09 | 通过 |
| 175 | physical N=12 J2=0.0 chi=8 growth 4 | wrong boundary operators, charge sectors, right-block reversal | -5.14205733732 | -5.14205733732 | 2e-09 | 通过 |
| 176 | physical N=14 J2=0.0 chi=8 growth 5 | wrong boundary operators, charge sectors, right-block reversal | -6.0266283086 | -6.0266283086 | 2e-09 | 通过 |
| 177 | physical N=16 J2=0.0 chi=8 growth 6 | wrong boundary operators, charge sectors, right-block reversal | -6.91157079643 | -6.91157079643 | 2e-09 | 通过 |
| 178 | physical N=18 J2=0.0 chi=8 growth 7 | wrong boundary operators, charge sectors, right-block reversal | -7.79671096958 | -7.79671096958 | 2e-09 | 通过 |
| 179 | physical N=20 J2=0.0 chi=8 growth 8 | wrong boundary operators, charge sectors, right-block reversal | -8.68204235035 | -8.68204235035 | 2e-09 | 通过 |
| 180 | physical N=20 J2=0.0 chi=8 sweep 0 | wrong boundary operators, charge sectors, right-block reversal | -8.68207985774 | -8.68207985774 | 2e-09 | 通过 |
| 181 | physical N=20 J2=0.0 chi=8 sweep 1 | wrong boundary operators, charge sectors, right-block reversal | -8.68207966282 | -8.68207966282 | 2e-09 | 通过 |
| 182 | physical N=20 J2=0.0 chi=8 sweep 2 | wrong boundary operators, charge sectors, right-block reversal | -8.68207966244 | -8.68207966244 | 2e-09 | 通过 |
| 183 | chi cap J2=0.0 chi=8 | per-sector cap erroneously multiplies total dimension | 0 | 0 | 0 | 通过 |
| 184 | projection loss J2=0.0 chi=8 | discard weight or selected singular vectors | 0 | 1.10138000066e-15 | 2e-12 | 通过 |
| 185 | charge retention J2=0.0 chi=8 | mixing charge sectors in truncation | 0 | 0 | 2e-12 | 通过 |
| 186 | isometry J2=0.0 chi=8 | nonorthogonal projected basis | 0 | 2.47439958135e-15 | 2e-11 | 通过 |
| 187 | local eigensolver J2=0.0 chi=8 | unconverged superblock solver (auxiliary) | 0 | 8.74071138622e-12 | 2e-08 | 通过 |
| 188 | physical N=4 J2=0.0 chi=16 growth 0 | wrong boundary operators, charge sectors, right-block reversal | -1.61602540378 | -1.61602540378 | 2e-09 | 通过 |
| 189 | physical N=6 J2=0.0 chi=16 growth 1 | wrong boundary operators, charge sectors, right-block reversal | -2.49357713389 | -2.49357713389 | 2e-09 | 通过 |
| 190 | physical N=8 J2=0.0 chi=16 growth 2 | wrong boundary operators, charge sectors, right-block reversal | -3.37493259869 | -3.37493259869 | 2e-09 | 通过 |
| 191 | physical N=10 J2=0.0 chi=16 growth 3 | wrong boundary operators, charge sectors, right-block reversal | -4.25803520728 | -4.25803520728 | 2e-09 | 通过 |
| 192 | physical N=12 J2=0.0 chi=16 growth 4 | wrong boundary operators, charge sectors, right-block reversal | -5.14209061201 | -5.14209061201 | 2e-09 | 通过 |
| 193 | physical N=14 J2=0.0 chi=16 growth 5 | wrong boundary operators, charge sectors, right-block reversal | -6.02672404941 | -6.02672404941 | 2e-09 | 通过 |
| 194 | physical N=16 J2=0.0 chi=16 growth 6 | wrong boundary operators, charge sectors, right-block reversal | -6.91173548026 | -6.91173548026 | 2e-09 | 通过 |
| 195 | physical N=18 J2=0.0 chi=16 growth 7 | wrong boundary operators, charge sectors, right-block reversal | -7.79700648781 | -7.79700648781 | 2e-09 | 通过 |
| 196 | physical N=20 J2=0.0 chi=16 growth 8 | wrong boundary operators, charge sectors, right-block reversal | -8.68246543654 | -8.68246543654 | 2e-09 | 通过 |
| 197 | physical N=20 J2=0.0 chi=16 sweep 0 | wrong boundary operators, charge sectors, right-block reversal | -8.68246958897 | -8.68246958897 | 2e-09 | 通过 |
| 198 | physical N=20 J2=0.0 chi=16 sweep 1 | wrong boundary operators, charge sectors, right-block reversal | -8.68246958741 | -8.68246958741 | 2e-09 | 通过 |
| 199 | physical N=20 J2=0.0 chi=16 sweep 2 | wrong boundary operators, charge sectors, right-block reversal | -8.68246958741 | -8.68246958741 | 2e-09 | 通过 |
| 200 | chi cap J2=0.0 chi=16 | per-sector cap erroneously multiplies total dimension | 0 | 0 | 0 | 通过 |
| 201 | projection loss J2=0.0 chi=16 | discard weight or selected singular vectors | 0 | 2.33677509254e-15 | 2e-12 | 通过 |
| 202 | charge retention J2=0.0 chi=16 | mixing charge sectors in truncation | 0 | 0 | 2e-12 | 通过 |
| 203 | isometry J2=0.0 chi=16 | nonorthogonal projected basis | 0 | 3.74283855446e-15 | 2e-11 | 通过 |
| 204 | local eigensolver J2=0.0 chi=16 | unconverged superblock solver (auxiliary) | 0 | 1.22655603198e-11 | 2e-08 | 通过 |
| 205 | physical N=4 J2=0.0 chi=32 growth 0 | wrong boundary operators, charge sectors, right-block reversal | -1.61602540378 | -1.61602540378 | 2e-09 | 通过 |
| 206 | physical N=6 J2=0.0 chi=32 growth 1 | wrong boundary operators, charge sectors, right-block reversal | -2.49357713389 | -2.49357713389 | 2e-09 | 通过 |
| 207 | physical N=8 J2=0.0 chi=32 growth 2 | wrong boundary operators, charge sectors, right-block reversal | -3.37493259869 | -3.37493259869 | 2e-09 | 通过 |
| 208 | physical N=10 J2=0.0 chi=32 growth 3 | wrong boundary operators, charge sectors, right-block reversal | -4.25803520728 | -4.25803520728 | 2e-09 | 通过 |
| 209 | physical N=12 J2=0.0 chi=32 growth 4 | wrong boundary operators, charge sectors, right-block reversal | -5.14209063284 | -5.14209063284 | 2e-09 | 通过 |
| 210 | physical N=14 J2=0.0 chi=32 growth 5 | wrong boundary operators, charge sectors, right-block reversal | -6.02672466183 | -6.02672466183 | 2e-09 | 通过 |
| 211 | physical N=16 J2=0.0 chi=32 growth 6 | wrong boundary operators, charge sectors, right-block reversal | -6.91173713789 | -6.91173713789 | 2e-09 | 通过 |
| 212 | physical N=18 J2=0.0 chi=32 growth 7 | wrong boundary operators, charge sectors, right-block reversal | -7.79701104346 | -7.79701104346 | 2e-09 | 通过 |
| 213 | physical N=20 J2=0.0 chi=32 growth 8 | wrong boundary operators, charge sectors, right-block reversal | -8.68247327445 | -8.68247327445 | 2e-09 | 通过 |
| 214 | physical N=20 J2=0.0 chi=32 sweep 0 | wrong boundary operators, charge sectors, right-block reversal | -8.68247332009 | -8.68247332009 | 2e-09 | 通过 |
| 215 | physical N=20 J2=0.0 chi=32 sweep 1 | wrong boundary operators, charge sectors, right-block reversal | -8.68247332009 | -8.68247332009 | 2e-09 | 通过 |
| 216 | chi cap J2=0.0 chi=32 | per-sector cap erroneously multiplies total dimension | 0 | 0 | 0 | 通过 |
| 217 | projection loss J2=0.0 chi=32 | discard weight or selected singular vectors | 0 | 1.8757703173e-15 | 2e-12 | 通过 |
| 218 | charge retention J2=0.0 chi=32 | mixing charge sectors in truncation | 0 | 0 | 2e-12 | 通过 |
| 219 | isometry J2=0.0 chi=32 | nonorthogonal projected basis | 0 | 5.62300620693e-15 | 2e-11 | 通过 |
| 220 | local eigensolver J2=0.0 chi=32 | unconverged superblock solver (auxiliary) | 0 | 6.73655556006e-12 | 2e-08 | 通过 |
| 221 | physical N=4 J2=0.3 chi=32 growth 0 | wrong boundary operators, charge sectors, right-block reversal | -1.52449979984 | -1.52449979984 | 2e-09 | 通过 |
| 222 | physical N=6 J2=0.3 chi=32 growth 1 | wrong boundary operators, charge sectors, right-block reversal | -2.30477549532 | -2.30477549532 | 2e-09 | 通过 |
| 223 | physical N=8 J2=0.3 chi=32 growth 2 | wrong boundary operators, charge sectors, right-block reversal | -3.08744625787 | -3.08744625787 | 2e-09 | 通过 |
| 224 | physical N=10 J2=0.3 chi=32 growth 3 | wrong boundary operators, charge sectors, right-block reversal | -3.87130470748 | -3.87130470748 | 2e-09 | 通过 |
| 225 | ED Hermitian N=12 J2=0.3 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 226 | ED residual N=12 J2=0.3 P=False | eigensolver convergence (auxiliary) | 0 | 8.28473079818e-14 | 2e-08 | 通过 |
| 227 | physical N=12 J2=0.3 chi=32 growth 4 | wrong boundary operators, charge sectors, right-block reversal | -4.65583299149 | -4.65583299149 | 2e-09 | 通过 |
| 228 | ED Hermitian N=14 J2=0.3 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 229 | ED residual N=14 J2=0.3 P=False | eigensolver convergence (auxiliary) | 0 | 8.94791939152e-15 | 2e-08 | 通过 |
| 230 | physical N=14 J2=0.3 chi=32 growth 5 | wrong boundary operators, charge sectors, right-block reversal | -5.4407751694 | -5.4407751694 | 2e-09 | 通过 |
| 231 | ED Hermitian N=16 J2=0.3 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 232 | ED residual N=16 J2=0.3 P=False | eigensolver convergence (auxiliary) | 0 | 2.24828779848e-13 | 2e-08 | 通过 |
| 233 | physical N=16 J2=0.3 chi=32 growth 6 | wrong boundary operators, charge sectors, right-block reversal | -6.22599068267 | -6.22599068267 | 2e-09 | 通过 |
| 234 | ED Hermitian N=18 J2=0.3 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 235 | ED residual N=18 J2=0.3 P=False | eigensolver convergence (auxiliary) | 0 | 1.51091104277e-14 | 2e-08 | 通过 |
| 236 | physical N=18 J2=0.3 chi=32 growth 7 | wrong boundary operators, charge sectors, right-block reversal | -7.01139603156 | -7.01139603156 | 2e-09 | 通过 |
| 237 | ED Hermitian N=20 J2=0.3 P=False | asymmetric matrix elements | 0 | 0 | 1e-14 | 通过 |
| 238 | ED residual N=20 J2=0.3 P=False | eigensolver convergence (auxiliary) | 0 | 6.02398488991e-13 | 2e-08 | 通过 |
| 239 | ED tensor action N=20 J2=0.3 P=False | wrong bonds, spin normalization, transverse sign, boundary | 0 | 4.21403680257e-15 | 1e-11 | 通过 |
| 240 | physical N=20 J2=0.3 chi=32 growth 8 | wrong boundary operators, charge sectors, right-block reversal | -7.79693852671 | -7.79693852671 | 2e-09 | 通过 |
| 241 | physical N=20 J2=0.3 chi=32 sweep 0 | wrong boundary operators, charge sectors, right-block reversal | -7.7969385432 | -7.7969385432 | 2e-09 | 通过 |
| 242 | physical N=20 J2=0.3 chi=32 sweep 1 | wrong boundary operators, charge sectors, right-block reversal | -7.7969385432 | -7.7969385432 | 2e-09 | 通过 |
| 243 | chi cap J2=0.3 chi=32 | per-sector cap erroneously multiplies total dimension | 0 | 0 | 0 | 通过 |
| 244 | projection loss J2=0.3 chi=32 | discard weight or selected singular vectors | 0 | 2.22044604925e-15 | 2e-12 | 通过 |
| 245 | charge retention J2=0.3 chi=32 | mixing charge sectors in truncation | 0 | 0 | 2e-12 | 通过 |
| 246 | isometry J2=0.3 chi=32 | nonorthogonal projected basis | 0 | 5.14897710903e-15 | 2e-11 | 通过 |
| 247 | local eigensolver J2=0.3 chi=32 | unconverged superblock solver (auxiliary) | 0 | 1.31012733464e-11 | 2e-08 | 通过 |
| 248 | mutation caught omit J2 | check sensitivity to deliberate Hamiltonian corruption | 1 | 1 | 0 | 通过 |
| 249 | mutation caught periodic wrap | check sensitivity to deliberate Hamiltonian corruption | 1 | 1 | 0 | 通过 |
| 250 | mutation caught wrong J2 sign | check sensitivity to deliberate Hamiltonian corruption | 1 | 1 | 0 | 通过 |
| 251 | mutation caught second edge zero | missing second edge operator | 1 | 1 | 0 | 通过 |
| 252 | entropy mirror J2=0.0 | incorrect left/right partition | 0 | 1.22124532709e-15 | 2e-10 | 通过 |
| 253 | entropy rho J2=0.0 | incorrect singular-value weights | 0 | 5.44009282066e-15 | 2e-10 | 通过 |
| 254 | entropy mirror J2=0.5 | incorrect left/right partition | 0 | 8.881784197e-16 | 2e-10 | 通过 |
| 255 | entropy rho J2=0.5 | incorrect singular-value weights | 0 | 1.22124532709e-15 | 2e-10 | 通过 |
| 256 | typical entropy product N=4 | entropy implementation | 0 | 2.22044604925e-16 | 2e-10 | 通过 |
| 257 | typical analytic product N=4 | state construction | 0 | 0 | 2e-12 | 通过 |
| 258 | typical entropy Neel N=4 | entropy implementation | 0 | 0 | 2e-10 | 通过 |
| 259 | typical analytic Neel N=4 | state construction | 0 | 0 | 2e-12 | 通过 |
| 260 | typical entropy GHZ N=4 | entropy implementation | 0.69314718056 | 0.69314718056 | 2e-10 | 通过 |
| 261 | typical analytic GHZ N=4 | state construction | 0.69314718056 | 0.69314718056 | 2e-12 | 通过 |
| 262 | typical entropy random N=4 | entropy implementation | 0.907417827419 | 0.907417827419 | 2e-10 | 通过 |
| 263 | typical entropy product N=8 | entropy implementation | 0 | 0 | 2e-10 | 通过 |
| 264 | typical analytic product N=8 | state construction | 0 | 0 | 2e-12 | 通过 |
| 265 | typical entropy Neel N=8 | entropy implementation | 0 | 0 | 2e-10 | 通过 |
| 266 | typical analytic Neel N=8 | state construction | 0 | 0 | 2e-12 | 通过 |
| 267 | typical entropy GHZ N=8 | entropy implementation | 0.69314718056 | 0.69314718056 | 2e-10 | 通过 |
| 268 | typical analytic GHZ N=8 | state construction | 0.69314718056 | 0.69314718056 | 2e-12 | 通过 |
| 269 | typical entropy random N=8 | entropy implementation | 2.23430205829 | 2.23430205829 | 2e-10 | 通过 |
| 270 | typical entropy product N=12 | entropy implementation | 0 | -2.22044604925e-16 | 2e-10 | 通过 |
| 271 | typical analytic product N=12 | state construction | 0 | 0 | 2e-12 | 通过 |
| 272 | typical entropy Neel N=12 | entropy implementation | 0 | 0 | 2e-10 | 通过 |
| 273 | typical analytic Neel N=12 | state construction | 0 | 0 | 2e-12 | 通过 |
| 274 | typical entropy GHZ N=12 | entropy implementation | 0.69314718056 | 0.69314718056 | 2e-10 | 通过 |
| 275 | typical analytic GHZ N=12 | state construction | 0.69314718056 | 0.69314718056 | 2e-12 | 通过 |
| 276 | typical entropy random N=12 | entropy implementation | 3.65431980623 | 3.65431980623 | 2e-10 | 通过 |
| 277 | typical entropy product N=16 | entropy implementation | 1.7763568394e-15 | 3.37208206925e-14 | 2e-10 | 通过 |
| 278 | typical analytic product N=16 | state construction | 0 | 1.7763568394e-15 | 2e-12 | 通过 |
| 279 | typical entropy Neel N=16 | entropy implementation | 0 | 0 | 2e-10 | 通过 |
| 280 | typical analytic Neel N=16 | state construction | 0 | 0 | 2e-12 | 通过 |
| 281 | typical entropy GHZ N=16 | entropy implementation | 0.69314718056 | 0.69314718056 | 2e-10 | 通过 |
| 282 | typical analytic GHZ N=16 | state construction | 0.69314718056 | 0.69314718056 | 2e-12 | 通过 |
| 283 | typical entropy random N=16 | entropy implementation | 5.0431630756 | 5.0431630756 | 2e-10 | 通过 |
| 284 | linear extrapolation independent solve | incorrect fit coordinates or intercept | -8.69080822261 | -8.69080822261 | 1e-11 | 通过 |
| 285 | optional convergence N=40 J2=0.0 chi=32 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 286 | optional chi cap N=40 J2=0.0 chi=32 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 287 | optional truncation N=40 J2=0.0 chi=32 | Schmidt weights do not equal projection loss | 0 | 2.71833016938e-15 | 3e-12 | 通过 |
| 288 | optional charge N=40 J2=0.0 chi=32 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 289 | optional local residual N=40 J2=0.0 chi=32 | unconverged local solve (auxiliary) | 0 | 3.30150671752e-11 | 5e-08 | 通过 |
| 290 | optional physical MPS N=40 J2=0.0 chi=32 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -17.541472114 | -17.541472114 | 5e-09 | 通过 |
| 291 | optional MPS norm N=40 J2=0.0 chi=32 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 292 | optional physical MPS N=40 J2=0.0 chi=32 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -17.5414721138 | -17.5414721138 | 5e-09 | 通过 |
| 293 | optional MPS norm N=40 J2=0.0 chi=32 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 294 | optional convergence N=40 J2=0.0 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 295 | optional chi cap N=40 J2=0.0 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 296 | optional truncation N=40 J2=0.0 chi=64 | Schmidt weights do not equal projection loss | 0 | 2.91706396196e-15 | 3e-12 | 通过 |
| 297 | optional charge N=40 J2=0.0 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 298 | optional local residual N=40 J2=0.0 chi=64 | unconverged local solve (auxiliary) | 0 | 1.48179245252e-11 | 5e-08 | 通过 |
| 299 | optional physical MPS N=40 J2=0.0 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -17.5414732984 | -17.5414732984 | 5e-09 | 通过 |
| 300 | optional MPS norm N=40 J2=0.0 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 301 | optional physical MPS N=40 J2=0.0 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -17.5414732984 | -17.5414732984 | 5e-09 | 通过 |
| 302 | optional MPS norm N=40 J2=0.0 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 303 | optional convergence N=60 J2=0.0 chi=32 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 304 | optional chi cap N=60 J2=0.0 chi=32 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 305 | optional truncation N=60 J2=0.0 chi=32 | Schmidt weights do not equal projection loss | 0 | 3.16927124712e-15 | 3e-12 | 通过 |
| 306 | optional charge N=60 J2=0.0 chi=32 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 307 | optional local residual N=60 J2=0.0 chi=32 | unconverged local solve (auxiliary) | 0 | 5.1756792231e-11 | 5e-08 | 通过 |
| 308 | optional physical MPS N=60 J2=0.0 chi=32 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -26.4030065765 | -26.4030065765 | 5e-09 | 通过 |
| 309 | optional MPS norm N=60 J2=0.0 chi=32 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 310 | optional physical MPS N=60 J2=0.0 chi=32 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -26.4030065729 | -26.4030065729 | 5e-09 | 通过 |
| 311 | optional MPS norm N=60 J2=0.0 chi=32 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 312 | optional physical MPS N=60 J2=0.0 chi=32 sweep=3 | renormalized H/edge errors, right reversal, missing physical bonds | -26.4030065729 | -26.4030065729 | 5e-09 | 通过 |
| 313 | optional MPS norm N=60 J2=0.0 chi=32 sweep=3 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 314 | optional convergence N=60 J2=0.0 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 315 | optional chi cap N=60 J2=0.0 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 316 | optional truncation N=60 J2=0.0 chi=64 | Schmidt weights do not equal projection loss | 0 | 3.58753227424e-15 | 3e-12 | 通过 |
| 317 | optional charge N=60 J2=0.0 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 318 | optional local residual N=60 J2=0.0 chi=64 | unconverged local solve (auxiliary) | 0 | 5.18056356302e-11 | 5e-08 | 通过 |
| 319 | optional physical MPS N=60 J2=0.0 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -26.4030151149 | -26.4030151149 | 5e-09 | 通过 |
| 320 | optional MPS norm N=60 J2=0.0 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 321 | optional physical MPS N=60 J2=0.0 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -26.4030151149 | -26.4030151149 | 5e-09 | 通过 |
| 322 | optional MPS norm N=60 J2=0.0 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 323 | dimer ED energy decomposition N=12 J2=0.0 | incorrect ED couplings or omitted physical bonds | -5.14209063284 | -5.14209063284 | 2e-10 | 通过 |
| 324 | dimer ED residual N=12 J2=0.0 | unconverged exact reference (auxiliary) | 0 | 1.78497622626e-15 | 5e-08 | 通过 |
| 325 | dimer central tensor N=12 J2=0.0 | central-bond positions, spin normalization, bit correlation errors | 0 | 5.55111512313e-17 | 2e-11 | 通过 |
| 326 | dimer ED energy decomposition N=16 J2=0.0 | incorrect ED couplings or omitted physical bonds | -6.91173714558 | -6.91173714558 | 2e-10 | 通过 |
| 327 | dimer ED residual N=16 J2=0.0 | unconverged exact reference (auxiliary) | 0 | 8.56633233135e-15 | 5e-08 | 通过 |
| 328 | dimer central tensor N=16 J2=0.0 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 329 | dimer ED energy decomposition N=20 J2=0.0 | incorrect ED couplings or omitted physical bonds | -8.6824733344 | -8.6824733344 | 2e-10 | 通过 |
| 330 | dimer ED residual N=20 J2=0.0 | unconverged exact reference (auxiliary) | 0 | 2.35854578253e-14 | 5e-08 | 通过 |
| 331 | dimer central tensor N=20 J2=0.0 | central-bond positions, spin normalization, bit correlation errors | 0 | 5.55111512313e-16 | 2e-11 | 通过 |
| 332 | optional convergence N=20 J2=0.0 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 333 | optional chi cap N=20 J2=0.0 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 334 | optional truncation N=20 J2=0.0 chi=64 | Schmidt weights do not equal projection loss | 0 | 1.22124532709e-15 | 3e-12 | 通过 |
| 335 | optional charge N=20 J2=0.0 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 336 | optional local residual N=20 J2=0.0 chi=64 | unconverged local solve (auxiliary) | 0 | 1.53207573786e-11 | 5e-08 | 通过 |
| 337 | optional physical MPS N=20 J2=0.0 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -8.6824733344 | -8.6824733344 | 5e-09 | 通过 |
| 338 | optional MPS norm N=20 J2=0.0 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 339 | optional physical MPS N=20 J2=0.0 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -8.6824733344 | -8.6824733344 | 5e-09 | 通过 |
| 340 | optional MPS norm N=20 J2=0.0 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 341 | dimer MPS vs physical bit bonds J2=0.0 | MPS local transfer, operator insertion or physical site ordering | 0 | 1.44328993201e-15 | 3e-11 | 通过 |
| 342 | dimer DMRG vs ED energy J2=0.0 | wrong variational ground state or inadequate chi | -8.6824733344 | -8.6824733344 | 2e-05 | 通过 |
| 343 | dimer DMRG vs ED all bonds J2=0.0 | incorrect or insufficiently converged dimer correlations | 0 | 5.05201436241e-12 | 0.0003 | 通过 |
| 344 | dimer ED energy decomposition N=12 J2=0.1 | incorrect ED couplings or omitted physical bonds | -4.96489999764 | -4.96489999764 | 2e-10 | 通过 |
| 345 | dimer ED residual N=12 J2=0.1 | unconverged exact reference (auxiliary) | 0 | 8.93247265367e-15 | 5e-08 | 通过 |
| 346 | dimer central tensor N=12 J2=0.1 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 347 | dimer ED energy decomposition N=16 J2=0.1 | incorrect ED couplings or omitted physical bonds | -6.66338692329 | -6.66338692329 | 2e-10 | 通过 |
| 348 | dimer ED residual N=16 J2=0.1 | unconverged exact reference (auxiliary) | 0 | 9.45492232587e-15 | 5e-08 | 通过 |
| 349 | dimer central tensor N=16 J2=0.1 | central-bond positions, spin normalization, bit correlation errors | 0 | 2.22044604925e-16 | 2e-11 | 通过 |
| 350 | dimer ED energy decomposition N=20 J2=0.1 | incorrect ED couplings or omitted physical bonds | -8.36295095093 | -8.36295095093 | 2e-10 | 通过 |
| 351 | dimer ED residual N=20 J2=0.1 | unconverged exact reference (auxiliary) | 0 | 2.07096337258e-14 | 5e-08 | 通过 |
| 352 | dimer central tensor N=20 J2=0.1 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.44328993201e-15 | 2e-11 | 通过 |
| 353 | optional convergence N=20 J2=0.1 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 354 | optional chi cap N=20 J2=0.1 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 355 | optional truncation N=20 J2=0.1 chi=64 | Schmidt weights do not equal projection loss | 0 | 2.58780936567e-15 | 3e-12 | 通过 |
| 356 | optional charge N=20 J2=0.1 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 357 | optional local residual N=20 J2=0.1 chi=64 | unconverged local solve (auxiliary) | 0 | 1.31390654784e-11 | 5e-08 | 通过 |
| 358 | optional physical MPS N=20 J2=0.1 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -8.36295095093 | -8.36295095093 | 5e-09 | 通过 |
| 359 | optional MPS norm N=20 J2=0.1 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 360 | optional physical MPS N=20 J2=0.1 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -8.36295095093 | -8.36295095093 | 5e-09 | 通过 |
| 361 | optional MPS norm N=20 J2=0.1 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 362 | dimer MPS vs physical bit bonds J2=0.1 | MPS local transfer, operator insertion or physical site ordering | 0 | 2.44249065418e-15 | 3e-11 | 通过 |
| 363 | dimer DMRG vs ED energy J2=0.1 | wrong variational ground state or inadequate chi | -8.36295095093 | -8.36295095093 | 2e-05 | 通过 |
| 364 | dimer DMRG vs ED all bonds J2=0.1 | incorrect or insufficiently converged dimer correlations | 0 | 3.91670029742e-12 | 0.0003 | 通过 |
| 365 | dimer ED energy decomposition N=12 J2=0.2 | incorrect ED couplings or omitted physical bonds | -4.80051062281 | -4.80051062281 | 2e-10 | 通过 |
| 366 | dimer ED residual N=12 J2=0.2 | unconverged exact reference (auxiliary) | 0 | 1.09766083938e-14 | 5e-08 | 通过 |
| 367 | dimer central tensor N=12 J2=0.2 | central-bond positions, spin normalization, bit correlation errors | 0 | 5.55111512313e-17 | 2e-11 | 通过 |
| 368 | dimer ED energy decomposition N=16 J2=0.2 | incorrect ED couplings or omitted physical bonds | -6.43180612955 | -6.43180612955 | 2e-10 | 通过 |
| 369 | dimer ED residual N=16 J2=0.2 | unconverged exact reference (auxiliary) | 0 | 1.59970975273e-14 | 5e-08 | 通过 |
| 370 | dimer central tensor N=16 J2=0.2 | central-bond positions, spin normalization, bit correlation errors | 0 | 2.22044604925e-16 | 2e-11 | 通过 |
| 371 | dimer ED energy decomposition N=20 J2=0.2 | incorrect ED couplings or omitted physical bonds | -8.06412144391 | -8.06412144391 | 2e-10 | 通过 |
| 372 | dimer ED residual N=20 J2=0.2 | unconverged exact reference (auxiliary) | 0 | 4.10922235005e-14 | 5e-08 | 通过 |
| 373 | dimer central tensor N=20 J2=0.2 | central-bond positions, spin normalization, bit correlation errors | 0 | 3.88578058619e-16 | 2e-11 | 通过 |
| 374 | optional convergence N=20 J2=0.2 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 375 | optional chi cap N=20 J2=0.2 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 376 | optional truncation N=20 J2=0.2 chi=64 | Schmidt weights do not equal projection loss | 0 | 2.51530336988e-15 | 3e-12 | 通过 |
| 377 | optional charge N=20 J2=0.2 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 378 | optional local residual N=20 J2=0.2 chi=64 | unconverged local solve (auxiliary) | 0 | 1.33036948884e-11 | 5e-08 | 通过 |
| 379 | optional physical MPS N=20 J2=0.2 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -8.06412144391 | -8.06412144391 | 5e-09 | 通过 |
| 380 | optional MPS norm N=20 J2=0.2 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 381 | optional physical MPS N=20 J2=0.2 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -8.06412144391 | -8.06412144391 | 5e-09 | 通过 |
| 382 | optional MPS norm N=20 J2=0.2 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 383 | dimer MPS vs physical bit bonds J2=0.2 | MPS local transfer, operator insertion or physical site ordering | 0 | 6.66133814775e-16 | 3e-11 | 通过 |
| 384 | dimer DMRG vs ED energy J2=0.2 | wrong variational ground state or inadequate chi | -8.06412144391 | -8.06412144391 | 2e-05 | 通过 |
| 385 | dimer DMRG vs ED all bonds J2=0.2 | incorrect or insufficiently converged dimer correlations | 0 | 2.84156032038e-12 | 0.0003 | 通过 |
| 386 | dimer ED energy decomposition N=12 J2=0.3 | incorrect ED couplings or omitted physical bonds | -4.65583299149 | -4.65583299149 | 2e-10 | 通过 |
| 387 | dimer ED residual N=12 J2=0.3 | unconverged exact reference (auxiliary) | 0 | 8.28473079818e-14 | 5e-08 | 通过 |
| 388 | dimer central tensor N=12 J2=0.3 | central-bond positions, spin normalization, bit correlation errors | 0 | 5.55111512313e-17 | 2e-11 | 通过 |
| 389 | dimer ED energy decomposition N=16 J2=0.3 | incorrect ED couplings or omitted physical bonds | -6.22599068592 | -6.22599068592 | 2e-10 | 通过 |
| 390 | dimer ED residual N=16 J2=0.3 | unconverged exact reference (auxiliary) | 0 | 2.24828779848e-13 | 5e-08 | 通过 |
| 391 | dimer central tensor N=16 J2=0.3 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 392 | dimer ED energy decomposition N=20 J2=0.3 | incorrect ED couplings or omitted physical bonds | -7.79693854521 | -7.79693854521 | 2e-10 | 通过 |
| 393 | dimer ED residual N=20 J2=0.3 | unconverged exact reference (auxiliary) | 0 | 6.02398488991e-13 | 5e-08 | 通过 |
| 394 | dimer central tensor N=20 J2=0.3 | central-bond positions, spin normalization, bit correlation errors | 0 | 9.99200722163e-16 | 2e-11 | 通过 |
| 395 | optional convergence N=20 J2=0.3 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 396 | optional chi cap N=20 J2=0.3 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 397 | optional truncation N=20 J2=0.3 chi=64 | Schmidt weights do not equal projection loss | 0 | 3.13475195593e-15 | 3e-12 | 通过 |
| 398 | optional charge N=20 J2=0.3 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 399 | optional local residual N=20 J2=0.3 chi=64 | unconverged local solve (auxiliary) | 0 | 1.49917286591e-11 | 5e-08 | 通过 |
| 400 | optional physical MPS N=20 J2=0.3 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -7.79693854521 | -7.79693854521 | 5e-09 | 通过 |
| 401 | optional MPS norm N=20 J2=0.3 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 402 | optional physical MPS N=20 J2=0.3 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -7.79693854521 | -7.79693854521 | 5e-09 | 通过 |
| 403 | optional MPS norm N=20 J2=0.3 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 404 | dimer MPS vs physical bit bonds J2=0.3 | MPS local transfer, operator insertion or physical site ordering | 0 | 9.99200722163e-16 | 3e-11 | 通过 |
| 405 | dimer DMRG vs ED energy J2=0.3 | wrong variational ground state or inadequate chi | -7.79693854521 | -7.79693854521 | 2e-05 | 通过 |
| 406 | dimer DMRG vs ED all bonds J2=0.3 | incorrect or insufficiently converged dimer correlations | 0 | 1.09094955292e-11 | 0.0003 | 通过 |
| 407 | dimer ED energy decomposition N=12 J2=0.4 | incorrect ED couplings or omitted physical bonds | -4.54562616266 | -4.54562616266 | 2e-10 | 通过 |
| 408 | dimer ED residual N=12 J2=0.4 | unconverged exact reference (auxiliary) | 0 | 8.0158348275e-13 | 5e-08 | 通过 |
| 409 | dimer central tensor N=12 J2=0.4 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 410 | dimer ED energy decomposition N=16 J2=0.4 | incorrect ED couplings or omitted physical bonds | -6.066665572 | -6.066665572 | 2e-10 | 通过 |
| 411 | dimer ED residual N=16 J2=0.4 | unconverged exact reference (auxiliary) | 0 | 3.62030433665e-12 | 5e-08 | 通过 |
| 412 | dimer central tensor N=16 J2=0.4 | central-bond positions, spin normalization, bit correlation errors | 0 | 3.33066907388e-16 | 2e-11 | 通过 |
| 413 | dimer ED energy decomposition N=20 J2=0.4 | incorrect ED couplings or omitted physical bonds | -7.58794101541 | -7.58794101541 | 2e-10 | 通过 |
| 414 | dimer ED residual N=20 J2=0.4 | unconverged exact reference (auxiliary) | 0 | 5.07591056865e-12 | 5e-08 | 通过 |
| 415 | dimer central tensor N=20 J2=0.4 | central-bond positions, spin normalization, bit correlation errors | 0 | 2.44249065418e-15 | 2e-11 | 通过 |
| 416 | optional convergence N=20 J2=0.4 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 417 | optional chi cap N=20 J2=0.4 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 418 | optional truncation N=20 J2=0.4 chi=64 | Schmidt weights do not equal projection loss | 0 | 2.30585107569e-15 | 3e-12 | 通过 |
| 419 | optional charge N=20 J2=0.4 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 420 | optional local residual N=20 J2=0.4 chi=64 | unconverged local solve (auxiliary) | 0 | 1.28954968398e-11 | 5e-08 | 通过 |
| 421 | optional physical MPS N=20 J2=0.4 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -7.58794101541 | -7.58794101541 | 5e-09 | 通过 |
| 422 | optional MPS norm N=20 J2=0.4 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 423 | optional physical MPS N=20 J2=0.4 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -7.58794101541 | -7.58794101541 | 5e-09 | 通过 |
| 424 | optional MPS norm N=20 J2=0.4 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 425 | dimer MPS vs physical bit bonds J2=0.4 | MPS local transfer, operator insertion or physical site ordering | 0 | 2.55351295664e-15 | 3e-11 | 通过 |
| 426 | dimer DMRG vs ED energy J2=0.4 | wrong variational ground state or inadequate chi | -7.58794101541 | -7.58794101541 | 2e-05 | 通过 |
| 427 | dimer DMRG vs ED all bonds J2=0.4 | incorrect or insufficiently converged dimer correlations | 0 | 9.68450319938e-12 | 0.0003 | 通过 |
| 428 | dimer ED energy decomposition N=12 J2=0.5 | incorrect ED couplings or omitted physical bonds | -4.5 | -4.5 | 2e-10 | 通过 |
| 429 | dimer ED residual N=12 J2=0.5 | unconverged exact reference (auxiliary) | 0 | 4.02699546767e-12 | 5e-08 | 通过 |
| 430 | dimer central tensor N=12 J2=0.5 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 431 | dimer MG profile N=12 | wrong strong/weak bond placement | 0 | 3.37445343969e-13 | 2e-10 | 通过 |
| 432 | dimer ED energy decomposition N=16 J2=0.5 | incorrect ED couplings or omitted physical bonds | -6 | -6 | 2e-10 | 通过 |
| 433 | dimer ED residual N=16 J2=0.5 | unconverged exact reference (auxiliary) | 0 | 9.35393291894e-15 | 5e-08 | 通过 |
| 434 | dimer central tensor N=16 J2=0.5 | central-bond positions, spin normalization, bit correlation errors | 0 | 4.55364912444e-18 | 2e-11 | 通过 |
| 435 | dimer MG profile N=16 | wrong strong/weak bond placement | 0 | 1.84863843829e-15 | 2e-10 | 通过 |
| 436 | dimer ED energy decomposition N=20 J2=0.5 | incorrect ED couplings or omitted physical bonds | -7.5 | -7.5 | 2e-10 | 通过 |
| 437 | dimer ED residual N=20 J2=0.5 | unconverged exact reference (auxiliary) | 0 | 3.08947980363e-12 | 5e-08 | 通过 |
| 438 | dimer central tensor N=20 J2=0.5 | central-bond positions, spin normalization, bit correlation errors | 0 | 2.92734606598e-18 | 2e-11 | 通过 |
| 439 | dimer MG profile N=20 | wrong strong/weak bond placement | 0 | 3.19040033225e-13 | 2e-10 | 通过 |
| 440 | optional convergence N=20 J2=0.5 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 441 | optional chi cap N=20 J2=0.5 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 442 | optional truncation N=20 J2=0.5 chi=64 | Schmidt weights do not equal projection loss | 0 | 2.6645352591e-15 | 3e-12 | 通过 |
| 443 | optional charge N=20 J2=0.5 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 444 | optional local residual N=20 J2=0.5 chi=64 | unconverged local solve (auxiliary) | 0 | 1.19548020199e-11 | 5e-08 | 通过 |
| 445 | optional physical MPS N=20 J2=0.5 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -7.5 | -7.5 | 5e-09 | 通过 |
| 446 | optional MPS norm N=20 J2=0.5 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 447 | optional physical MPS N=20 J2=0.5 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -7.5 | -7.5 | 5e-09 | 通过 |
| 448 | optional MPS norm N=20 J2=0.5 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 449 | dimer MPS vs physical bit bonds J2=0.5 | MPS local transfer, operator insertion or physical site ordering | 0 | 3.33066907388e-16 | 3e-11 | 通过 |
| 450 | dimer DMRG vs ED energy J2=0.5 | wrong variational ground state or inadequate chi | -7.5 | -7.5 | 2e-05 | 通过 |
| 451 | dimer DMRG vs ED all bonds J2=0.5 | incorrect or insufficiently converged dimer correlations | 0 | 3.21942984972e-13 | 0.0003 | 通过 |
| 452 | dimer ED energy decomposition N=12 J2=0.6 | incorrect ED couplings or omitted physical bonds | -4.5540577684 | -4.5540577684 | 2e-10 | 通过 |
| 453 | dimer ED residual N=12 J2=0.6 | unconverged exact reference (auxiliary) | 0 | 2.38995333842e-12 | 5e-08 | 通过 |
| 454 | dimer central tensor N=12 J2=0.6 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 455 | dimer ED energy decomposition N=16 J2=0.6 | incorrect ED couplings or omitted physical bonds | -6.07729411043 | -6.07729411043 | 2e-10 | 通过 |
| 456 | dimer ED residual N=16 J2=0.6 | unconverged exact reference (auxiliary) | 0 | 2.95427456588e-12 | 5e-08 | 通过 |
| 457 | dimer central tensor N=16 J2=0.6 | central-bond positions, spin normalization, bit correlation errors | 0 | 6.66133814775e-16 | 2e-11 | 通过 |
| 458 | dimer ED energy decomposition N=20 J2=0.6 | incorrect ED couplings or omitted physical bonds | -7.60053356896 | -7.60053356896 | 2e-10 | 通过 |
| 459 | dimer ED residual N=20 J2=0.6 | unconverged exact reference (auxiliary) | 0 | 1.06746602837e-13 | 5e-08 | 通过 |
| 460 | dimer central tensor N=20 J2=0.6 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.66533453694e-15 | 2e-11 | 通过 |
| 461 | optional convergence N=20 J2=0.6 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 462 | optional chi cap N=20 J2=0.6 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 463 | optional truncation N=20 J2=0.6 chi=64 | Schmidt weights do not equal projection loss | 0 | 1.92848392756e-15 | 3e-12 | 通过 |
| 464 | optional charge N=20 J2=0.6 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 465 | optional local residual N=20 J2=0.6 chi=64 | unconverged local solve (auxiliary) | 0 | 1.47495507607e-11 | 5e-08 | 通过 |
| 466 | optional physical MPS N=20 J2=0.6 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -7.60053356891 | -7.60053356891 | 5e-09 | 通过 |
| 467 | optional MPS norm N=20 J2=0.6 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 468 | optional physical MPS N=20 J2=0.6 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -7.60053356891 | -7.60053356891 | 5e-09 | 通过 |
| 469 | optional MPS norm N=20 J2=0.6 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 470 | dimer MPS vs physical bit bonds J2=0.6 | MPS local transfer, operator insertion or physical site ordering | 0 | 1.66533453694e-15 | 3e-11 | 通过 |
| 471 | dimer DMRG vs ED energy J2=0.6 | wrong variational ground state or inadequate chi | -7.60053356896 | -7.60053356891 | 2e-05 | 通过 |
| 472 | dimer DMRG vs ED all bonds J2=0.6 | incorrect or insufficiently converged dimer correlations | 0 | 3.19980320018e-10 | 0.0003 | 通过 |
| 473 | dimer ED energy decomposition N=12 J2=0.7 | incorrect ED couplings or omitted physical bonds | -4.7132991111 | -4.7132991111 | 2e-10 | 通过 |
| 474 | dimer ED residual N=12 J2=0.7 | unconverged exact reference (auxiliary) | 0 | 1.02656364161e-12 | 5e-08 | 通过 |
| 475 | dimer central tensor N=12 J2=0.7 | central-bond positions, spin normalization, bit correlation errors | 0 | 2.77555756156e-17 | 2e-11 | 通过 |
| 476 | dimer ED energy decomposition N=16 J2=0.7 | incorrect ED couplings or omitted physical bonds | -6.30207333609 | -6.30207333609 | 2e-10 | 通过 |
| 477 | dimer ED residual N=16 J2=0.7 | unconverged exact reference (auxiliary) | 0 | 2.88199206599e-13 | 5e-08 | 通过 |
| 478 | dimer central tensor N=16 J2=0.7 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 479 | dimer ED energy decomposition N=20 J2=0.7 | incorrect ED couplings or omitted physical bonds | -7.89087125801 | -7.89087125801 | 2e-10 | 通过 |
| 480 | dimer ED residual N=20 J2=0.7 | unconverged exact reference (auxiliary) | 0 | 3.10089120491e-14 | 5e-08 | 通过 |
| 481 | dimer central tensor N=20 J2=0.7 | central-bond positions, spin normalization, bit correlation errors | 0 | 9.99200722163e-16 | 2e-11 | 通过 |
| 482 | optional convergence N=20 J2=0.7 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 483 | optional chi cap N=20 J2=0.7 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 484 | optional truncation N=20 J2=0.7 chi=64 | Schmidt weights do not equal projection loss | 0 | 2.02204414548e-15 | 3e-12 | 通过 |
| 485 | optional charge N=20 J2=0.7 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 486 | optional local residual N=20 J2=0.7 chi=64 | unconverged local solve (auxiliary) | 0 | 1.35817431578e-11 | 5e-08 | 通过 |
| 487 | optional physical MPS N=20 J2=0.7 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -7.89087125448 | -7.89087125448 | 5e-09 | 通过 |
| 488 | optional MPS norm N=20 J2=0.7 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 489 | optional physical MPS N=20 J2=0.7 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -7.89087125448 | -7.89087125448 | 5e-09 | 通过 |
| 490 | optional MPS norm N=20 J2=0.7 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 491 | dimer MPS vs physical bit bonds J2=0.7 | MPS local transfer, operator insertion or physical site ordering | 0 | 1.7763568394e-15 | 3e-11 | 通过 |
| 492 | dimer DMRG vs ED energy J2=0.7 | wrong variational ground state or inadequate chi | -7.89087125801 | -7.89087125448 | 2e-05 | 通过 |
| 493 | dimer DMRG vs ED all bonds J2=0.7 | incorrect or insufficiently converged dimer correlations | 0 | 1.81854883374e-08 | 0.0003 | 通过 |
| 494 | dimer ED energy decomposition N=12 J2=0.8 | incorrect ED couplings or omitted physical bonds | -4.9590448809 | -4.9590448809 | 2e-10 | 通过 |
| 495 | dimer ED residual N=12 J2=0.8 | unconverged exact reference (auxiliary) | 0 | 1.931136521e-12 | 5e-08 | 通过 |
| 496 | dimer central tensor N=12 J2=0.8 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 497 | dimer ED energy decomposition N=16 J2=0.8 | incorrect ED couplings or omitted physical bonds | -6.64579242916 | -6.64579242916 | 2e-10 | 通过 |
| 498 | dimer ED residual N=16 J2=0.8 | unconverged exact reference (auxiliary) | 0 | 3.0796658955e-13 | 5e-08 | 通过 |
| 499 | dimer central tensor N=16 J2=0.8 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 500 | dimer ED energy decomposition N=20 J2=0.8 | incorrect ED couplings or omitted physical bonds | -8.33261070619 | -8.33261070619 | 2e-10 | 通过 |
| 501 | dimer ED residual N=20 J2=0.8 | unconverged exact reference (auxiliary) | 0 | 3.63166203048e-14 | 5e-08 | 通过 |
| 502 | dimer central tensor N=20 J2=0.8 | central-bond positions, spin normalization, bit correlation errors | 0 | 6.66133814775e-16 | 2e-11 | 通过 |
| 503 | optional convergence N=20 J2=0.8 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 504 | optional chi cap N=20 J2=0.8 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 505 | optional truncation N=20 J2=0.8 chi=64 | Schmidt weights do not equal projection loss | 0 | 2.51780358841e-15 | 3e-12 | 通过 |
| 506 | optional charge N=20 J2=0.8 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 507 | optional local residual N=20 J2=0.8 chi=64 | unconverged local solve (auxiliary) | 0 | 1.50624749811e-11 | 5e-08 | 通过 |
| 508 | optional physical MPS N=20 J2=0.8 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -8.33261065131 | -8.33261065131 | 5e-09 | 通过 |
| 509 | optional MPS norm N=20 J2=0.8 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 510 | optional physical MPS N=20 J2=0.8 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -8.33261065131 | -8.33261065131 | 5e-09 | 通过 |
| 511 | optional MPS norm N=20 J2=0.8 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 512 | dimer MPS vs physical bit bonds J2=0.8 | MPS local transfer, operator insertion or physical site ordering | 0 | 1.99840144433e-15 | 3e-11 | 通过 |
| 513 | dimer DMRG vs ED energy J2=0.8 | wrong variational ground state or inadequate chi | -8.33261070619 | -8.33261065131 | 2e-05 | 通过 |
| 514 | dimer DMRG vs ED all bonds J2=0.8 | incorrect or insufficiently converged dimer correlations | 0 | 2.22157968355e-07 | 0.0003 | 通过 |
| 515 | dimer ED energy decomposition N=12 J2=0.9 | incorrect ED couplings or omitted physical bonds | -5.26855687072 | -5.26855687072 | 2e-10 | 通过 |
| 516 | dimer ED residual N=12 J2=0.9 | unconverged exact reference (auxiliary) | 0 | 5.08408211726e-15 | 5e-08 | 通过 |
| 517 | dimer central tensor N=12 J2=0.9 | central-bond positions, spin normalization, bit correlation errors | 0 | 5.55111512313e-17 | 2e-11 | 通过 |
| 518 | dimer ED energy decomposition N=16 J2=0.9 | incorrect ED couplings or omitted physical bonds | -7.07659025477 | -7.07659025477 | 2e-10 | 通过 |
| 519 | dimer ED residual N=16 J2=0.9 | unconverged exact reference (auxiliary) | 0 | 7.97881481873e-13 | 5e-08 | 通过 |
| 520 | dimer central tensor N=16 J2=0.9 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.66533453694e-16 | 2e-11 | 通过 |
| 521 | dimer ED energy decomposition N=20 J2=0.9 | incorrect ED couplings or omitted physical bonds | -8.88452050618 | -8.88452050618 | 2e-10 | 通过 |
| 522 | dimer ED residual N=20 J2=0.9 | unconverged exact reference (auxiliary) | 0 | 5.1778730212e-14 | 5e-08 | 通过 |
| 523 | dimer central tensor N=20 J2=0.9 | central-bond positions, spin normalization, bit correlation errors | 0 | 3.33066907388e-16 | 2e-11 | 通过 |
| 524 | optional convergence N=20 J2=0.9 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 525 | optional chi cap N=20 J2=0.9 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 526 | optional truncation N=20 J2=0.9 chi=64 | Schmidt weights do not equal projection loss | 0 | 2.22604959406e-15 | 3e-12 | 通过 |
| 527 | optional charge N=20 J2=0.9 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 528 | optional local residual N=20 J2=0.9 chi=64 | unconverged local solve (auxiliary) | 0 | 1.67958579191e-11 | 5e-08 | 通过 |
| 529 | optional physical MPS N=20 J2=0.9 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -8.88452024914 | -8.88452024914 | 5e-09 | 通过 |
| 530 | optional MPS norm N=20 J2=0.9 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 531 | optional physical MPS N=20 J2=0.9 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -8.884520249 | -8.884520249 | 5e-09 | 通过 |
| 532 | optional MPS norm N=20 J2=0.9 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 533 | dimer MPS vs physical bit bonds J2=0.9 | MPS local transfer, operator insertion or physical site ordering | 0 | 2.22044604925e-15 | 3e-11 | 通过 |
| 534 | dimer DMRG vs ED energy J2=0.9 | wrong variational ground state or inadequate chi | -8.88452050618 | -8.884520249 | 2e-05 | 通过 |
| 535 | dimer DMRG vs ED all bonds J2=0.9 | incorrect or insufficiently converged dimer correlations | 0 | 9.22752815824e-07 | 0.0003 | 通过 |
| 536 | dimer ED energy decomposition N=12 J2=1.0 | incorrect ED couplings or omitted physical bonds | -5.62421027774 | -5.62421027774 | 2e-10 | 通过 |
| 537 | dimer ED residual N=12 J2=1.0 | unconverged exact reference (auxiliary) | 0 | 3.25485608422e-12 | 5e-08 | 通过 |
| 538 | dimer central tensor N=12 J2=1.0 | central-bond positions, spin normalization, bit correlation errors | 0 | 5.55111512313e-17 | 2e-11 | 通过 |
| 539 | dimer ED energy decomposition N=16 J2=1.0 | incorrect ED couplings or omitted physical bonds | -7.56889475146 | -7.56889475146 | 2e-10 | 通过 |
| 540 | dimer ED residual N=16 J2=1.0 | unconverged exact reference (auxiliary) | 0 | 2.39419343023e-12 | 5e-08 | 通过 |
| 541 | dimer central tensor N=16 J2=1.0 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-16 | 2e-11 | 通过 |
| 542 | dimer ED energy decomposition N=20 J2=1.0 | incorrect ED couplings or omitted physical bonds | -9.51388442913 | -9.51388442913 | 2e-10 | 通过 |
| 543 | dimer ED residual N=20 J2=1.0 | unconverged exact reference (auxiliary) | 0 | 2.09320464892e-13 | 5e-08 | 通过 |
| 544 | dimer central tensor N=20 J2=1.0 | central-bond positions, spin normalization, bit correlation errors | 0 | 1.11022302463e-15 | 2e-11 | 通过 |
| 545 | optional convergence N=20 J2=1.0 chi=64 | fixed-chi energy iteration not converged | 1 | 1 | 0 | 通过 |
| 546 | optional chi cap N=20 J2=1.0 chi=64 | per-sector chi cap instead of global cap | 0 | 0 | 0 | 通过 |
| 547 | optional truncation N=20 J2=1.0 chi=64 | Schmidt weights do not equal projection loss | 0 | 2.33788294546e-15 | 3e-12 | 通过 |
| 548 | optional charge N=20 J2=1.0 chi=64 | charge mixing in selected singular vectors | 0 | 0 | 2e-12 | 通过 |
| 549 | optional local residual N=20 J2=1.0 chi=64 | unconverged local solve (auxiliary) | 0 | 1.29902157923e-11 | 5e-08 | 通过 |
| 550 | optional physical MPS N=20 J2=1.0 chi=64 sweep=1 | renormalized H/edge errors, right reversal, missing physical bonds | -9.51388383886 | -9.51388383886 | 5e-09 | 通过 |
| 551 | optional MPS norm N=20 J2=1.0 chi=64 sweep=1 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 552 | optional physical MPS N=20 J2=1.0 chi=64 sweep=2 | renormalized H/edge errors, right reversal, missing physical bonds | -9.5138838393 | -9.5138838393 | 5e-09 | 通过 |
| 553 | optional MPS norm N=20 J2=1.0 chi=64 sweep=2 | wrong saved isometries or MPS centre connection | 1 | 1 | 2e-10 | 通过 |
| 554 | dimer MPS vs physical bit bonds J2=1.0 | MPS local transfer, operator insertion or physical site ordering | 0 | 6.66133814775e-16 | 3e-11 | 通过 |
| 555 | dimer DMRG vs ED energy J2=1.0 | wrong variational ground state or inadequate chi | -9.51388442913 | -9.5138838393 | 2e-05 | 通过 |
| 556 | dimer DMRG vs ED all bonds J2=1.0 | incorrect or insufficiently converged dimer correlations | 0 | 1.6317327361e-06 | 0.0003 | 通过 |
| 557 | optional mutation wrong transverse coefficient | physical correlation check sensitivity | 1 | 1 | 0 | 通过 |
| 558 | scaling eps_max independent_power_difference | incorrect fit coordinates, coefficient or intercept | 0 | 2.22044604925e-16 | 1e-10 | 通过 |
| 559 | scaling eps_max independent_log_amplitude_difference | incorrect fit coordinates, coefficient or intercept | 0 | 1.33226762955e-15 | 1e-10 | 通过 |
| 560 | scaling eps_max independent_r2_difference | incorrect fit coordinates, coefficient or intercept | 0 | 2.22044604925e-16 | 1e-10 | 通过 |
| 561 | scaling eps_max independent_intercept_difference | incorrect fit coordinates, coefficient or intercept | 0 | 1.15535294005e-18 | 1e-10 | 通过 |
| 562 | scaling eps_max independent_slope_difference | incorrect fit coordinates, coefficient or intercept | 0 | 3.5527136788e-15 | 1e-10 | 通过 |
| 563 | scaling eps_centre independent_power_difference | incorrect fit coordinates, coefficient or intercept | 0 | 0 | 1e-10 | 通过 |
| 564 | scaling eps_centre independent_log_amplitude_difference | incorrect fit coordinates, coefficient or intercept | 0 | 7.1054273576e-15 | 1e-10 | 通过 |
| 565 | scaling eps_centre independent_r2_difference | incorrect fit coordinates, coefficient or intercept | 0 | 3.33066907388e-16 | 1e-10 | 通过 |
| 566 | scaling eps_centre independent_intercept_difference | incorrect fit coordinates, coefficient or intercept | 0 | 1.08420217249e-18 | 1e-10 | 通过 |
| 567 | scaling eps_centre independent_slope_difference | incorrect fit coordinates, coefficient or intercept | 0 | 1.13686837722e-13 | 1e-10 | 通过 |
| 568 | baseline N=12 J2=0.0 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0 | 0 | 2e-13 | 通过 |
| 569 | baseline N=16 J2=0.0 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0 | 0 | 2e-13 | 通过 |
| 570 | baseline N=20 J2=0.0 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0 | 0 | 2e-13 | 通过 |
| 571 | baseline N=20 J2=0.0 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0 | 0 | 2e-13 | 通过 |
| 572 | baseline N=12 J2=0.1 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.0453486505967 | 0.0453486505967 | 2e-13 | 通过 |
| 573 | baseline N=16 J2=0.1 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.0403917948105 | 0.0403917948105 | 2e-13 | 通过 |
| 574 | baseline N=20 J2=0.1 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.0366553365288 | 0.0366553365288 | 2e-13 | 通过 |
| 575 | baseline N=20 J2=0.1 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.0366553365282 | 0.0366553365282 | 2e-13 | 通过 |
| 576 | baseline N=12 J2=0.2 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.11235752322 | 0.11235752322 | 2e-13 | 通过 |
| 577 | baseline N=16 J2=0.2 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.103103100119 | 0.103103100119 | 2e-13 | 通过 |
| 578 | baseline N=20 J2=0.2 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.0955296804526 | 0.0955296804526 | 2e-13 | 通过 |
| 579 | baseline N=20 J2=0.2 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.0955296804552 | 0.0955296804552 | 2e-13 | 通过 |
| 580 | baseline N=12 J2=0.3 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.216479176696 | 0.216479176696 | 2e-13 | 通过 |
| 581 | baseline N=16 J2=0.3 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.209262883619 | 0.209262883619 | 2e-13 | 通过 |
| 582 | baseline N=20 J2=0.3 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.201861626551 | 0.201861626551 | 2e-13 | 通过 |
| 583 | baseline N=20 J2=0.3 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.201861626565 | 0.201861626565 | 2e-13 | 通过 |
| 584 | baseline N=12 J2=0.4 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.372559797898 | 0.372559797898 | 2e-13 | 通过 |
| 585 | baseline N=16 J2=0.4 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.38628450917 | 0.38628450917 | 2e-13 | 通过 |
| 586 | baseline N=20 J2=0.4 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.394912531736 | 0.394912531736 | 2e-13 | 通过 |
| 587 | baseline N=20 J2=0.4 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.394912531748 | 0.394912531748 | 2e-13 | 通过 |
| 588 | baseline N=12 J2=0.5 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.532522524423 | 0.532522524423 | 2e-13 | 通过 |
| 589 | baseline N=16 J2=0.5 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.567067647716 | 0.567067647716 | 2e-13 | 通过 |
| 590 | baseline N=20 J2=0.5 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.589971462329 | 0.589971462329 | 2e-13 | 通过 |
| 591 | baseline N=20 J2=0.5 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.589971462327 | 0.589971462327 | 2e-13 | 通过 |
| 592 | baseline N=12 J2=0.6 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.572540291264 | 0.572540291264 | 2e-13 | 通过 |
| 593 | baseline N=16 J2=0.6 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.605147116491 | 0.605147116491 | 2e-13 | 通过 |
| 594 | baseline N=20 J2=0.6 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.628378910069 | 0.628378910069 | 2e-13 | 通过 |
| 595 | baseline N=20 J2=0.6 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.628378910435 | 0.628378910435 | 2e-13 | 通过 |
| 596 | baseline N=12 J2=0.7 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.519339836959 | 0.519339836959 | 2e-13 | 通过 |
| 597 | baseline N=16 J2=0.7 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.556870073987 | 0.556870073987 | 2e-13 | 通过 |
| 598 | baseline N=20 J2=0.7 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.576583152821 | 0.576583152821 | 2e-13 | 通过 |
| 599 | baseline N=20 J2=0.7 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.576583178882 | 0.576583178882 | 2e-13 | 通过 |
| 600 | baseline N=12 J2=0.8 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.448863702669 | 0.448863702669 | 2e-13 | 通过 |
| 601 | baseline N=16 J2=0.8 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.478999164607 | 0.478999164607 | 2e-13 | 通过 |
| 602 | baseline N=20 J2=0.8 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.492292972058 | 0.492292972058 | 2e-13 | 通过 |
| 603 | baseline N=20 J2=0.8 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.492293257184 | 0.492293257184 | 2e-13 | 通过 |
| 604 | baseline N=12 J2=0.9 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.38864063154 | 0.38864063154 | 2e-13 | 通过 |
| 605 | baseline N=16 J2=0.9 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.392540586667 | 0.392540586667 | 2e-13 | 通过 |
| 606 | baseline N=20 J2=0.9 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.40897387957 | 0.40897387957 | 2e-13 | 通过 |
| 607 | baseline N=20 J2=0.9 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.408975339886 | 0.408975339886 | 2e-13 | 通过 |
| 608 | baseline N=12 J2=1.0 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.337253109962 | 0.337253109962 | 2e-13 | 通过 |
| 609 | baseline N=16 J2=1.0 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.312011743236 | 0.312011743236 | 2e-13 | 通过 |
| 610 | baseline N=20 J2=1.0 ED | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.341122142548 | 0.341122142548 | 2e-13 | 通过 |
| 611 | baseline N=20 J2=1.0 DMRG | mixing sizes/methods or swapping absolute value and baseline subtraction | 0.341124932428 | 0.341124932428 | 2e-13 | 通过 |
