
#The pandas .convert_objects() function is deprecated
#Couldnt get the new function to work properly, didnt want to waste more time on it
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy.stats import norm
import numpy as np
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.stats.multicomp
import probscale
import sys

#ANOVA
#Thanks to Marvin for Python help

if len(sys.argv) <= 5:
	print("Not enough args usage: anova.py <*.csv> <rv1,rv2> <factors> <replicates> <alpha> optional: device")
	print("ex: anova.py testdata.csv nicdrop,avg 5 10 .05 TX1")
	print("<rv> is response variable, note comma in example")
	print("\"Device\" is used in normplot of effects, omit to skip graph")
	exit()

n = int(sys.argv[4]) #replicates
k = int(sys.argv[3]) #factors
alpha = float(sys.argv[5])
rv = sys.argv[2].split(',')
input_csv_parse = sys.argv[1].split('-')


if k > 5 or k < 1:
	print("Max factors is 5, Min is 1")
	exit()


data2 = pd.read_csv(sys.argv[1], header=[0,1])
response_var = data2[[rv[0],'factors']]
response_var.columns = response_var.columns.get_level_values(1)
#print(response_var.groupby('code').mean().sort_values(by=[rv[1]]).round(0))

if(k >= 1):
	df_index=['A', 'Error', 'Total']
	one = response_var[response_var['code'] == 'N'].loc[:,rv[1]].to_numpy()
	a 	= response_var[response_var['code'] == 'A'].loc[:,rv[1]].to_numpy()
	means_all = np.array([np.mean(a)])
	total = np.array([one, a])
	contrast_A = np.sum(-one + a)
	contrasts_all = np.array([contrast_A])
if(k >= 2):
	df_index=['A', 'B', 'AB', 'Error', 'Total']
	one = response_var[response_var['code'] == 'N'].loc[:,rv[1]].to_numpy()
	a 	= response_var[response_var['code'] == 'A'].loc[:,rv[1]].to_numpy()
	b 	= response_var[response_var['code'] == 'B'].loc[:,rv[1]].to_numpy()
	ab 	= response_var[response_var['code'] == 'AB'].loc[:,rv[1]].to_numpy()
	means_all = np.array([np.mean(a), np.mean(b), np.mean(ab)])
	total = np.array([one, a, b, ab])
	contrast_A = np.sum(-one + a - b + ab)
	contrast_B = np.sum(-one - a + b + ab)
	contrast_AB = np.sum(one - a - b + ab)
	contrasts_all = np.array([contrast_A, contrast_B, contrast_AB])
if(k >= 3):
	df_index=['A', 'B', 'AB', 'C', 'AC', 'BC', 'ABC', 'Error', 'Total']
	c 	= response_var[response_var['code'] == 'C'].loc[:,rv[1]].to_numpy()
	ac 	= response_var[response_var['code'] == 'AC'].loc[:,rv[1]].to_numpy()
	bc 	= response_var[response_var['code'] == 'BC'].loc[:,rv[1]].to_numpy()
	abc = response_var[response_var['code'] == 'ABC'].loc[:,rv[1]].to_numpy()
	means_all = np.array([np.mean(a), np.mean(b), np.mean(ab), np.mean(c), np.mean(ac), np.mean(bc), np.mean(abc)])
	total = np.array([one, a, b, ab, c, ac, bc, abc])
	contrast_A = np.sum(-one + a - b + ab - c + ac - bc + abc)
	contrast_B = np.sum(-one - a + b + ab - c - ac + bc + abc)
	contrast_AB = np.sum(one - a - b + ab + c - ac - bc + abc)
	contrast_C = np.sum(-one - a - b - ab + c + ac + bc + abc)
	contrast_AC = np.sum(one - a + b - ab - c + ac - bc + abc)
	contrast_BC = np.sum(one + a - b - ab - c - ac + bc + abc)
	contrast_ABC= np.sum(-one+ a + b - ab + c - ac - bc + abc)
	contrasts_all = np.array([contrast_A, contrast_B, contrast_AB, contrast_C, contrast_AC, contrast_BC, contrast_ABC])
if(k >= 4):
	df_index=['A', 'B', 'AB', 'C', 'AC', 'BC', 'ABC', 'D', 'AD', 'BD', 'ABD', 'CD', 'ACD', 'BCD', 'ABCD', 'Error', 'Total']
	d 	= response_var[response_var['code'] == 'D'].loc[:,rv[1]].to_numpy()
	ad 	= response_var[response_var['code'] == 'AD'].loc[:,rv[1]].to_numpy()
	bd 	= response_var[response_var['code'] == 'BD'].loc[:,rv[1]].to_numpy()
	abd = response_var[response_var['code'] == 'ABD'].loc[:,rv[1]].to_numpy()
	cd 	= response_var[response_var['code'] == 'CD'].loc[:,rv[1]].to_numpy()
	acd = response_var[response_var['code'] == 'ACD'].loc[:,rv[1]].to_numpy()
	bcd = response_var[response_var['code'] == 'BCD'].loc[:,rv[1]].to_numpy()
	abcd = response_var[response_var['code'] == 'ABCD'].loc[:,rv[1]].to_numpy()
	means_all = np.array([np.mean(a), np.mean(b), np.mean(ab), np.mean(c), np.mean(ac), np.mean(bc), np.mean(abc), np.mean(d),
							np.mean(ad), np.mean(bd), np.mean(abd), np.mean(cd), np.mean(acd), np.mean(bcd), np.mean(abcd)])
	total = np.array([one, a, b, ab, c, ac, bc, abc, d, ad, bd, abd, cd, acd, bcd, abcd])
	contrast_A = np.sum(-one + a - b + ab - c + ac - bc + abc - d + ad - bd + abd - cd + acd - bcd + abcd)
	contrast_B = np.sum(-one - a + b + ab - c - ac + bc + abc - d - ad + bd + abd - cd - acd + bcd + abcd)
	contrast_AB = np.sum(one - a - b + ab + c - ac - bc + abc + d - ad - bd + abd + cd - acd - bcd + abcd)
	contrast_C = np.sum(-one - a - b - ab + c + ac + bc + abc - d - ad - bd - abd + cd + acd + bcd + abcd)
	contrast_AC = np.sum(one - a + b - ab - c + ac - bc + abc + d - ad + bd - abd - cd + acd - bcd + abcd)
	contrast_BC = np.sum(one + a - b - ab - c - ac + bc + abc + d + ad - bd - abd - cd - acd + bcd + abcd)
	contrast_ABC= np.sum(-one+ a + b - ab + c - ac - bc + abc - d + ad + bd - abd + cd - acd - bcd + abcd)
	contrast_D =  np.sum(-one- a - b - ab - c - ac - bc - abc + d + ad + bd + abd + cd + acd + bcd + abcd)
	contrast_AD=  np.sum(one - a + b - ab + c - ac + bc - abc - d + ad - bd + abd - cd + acd - bcd + abcd)
	contrast_BD = np.sum(one + a - b - ab + c + ac - bc - abc - d - ad + bd + abd - cd - acd + bcd + abcd)
	contrast_ABD= np.sum(-one + a + b - ab - c + ac + bc - abc + d - ad - bd + abd + cd - acd - bcd + abcd)
	contrast_CD = np.sum(one + a + b + ab - c - ac - bc - abc - d - ad - bd - abd + cd + acd + bcd + abcd)
	contrast_ACD = np.sum(-one + a - b + ab + c - ac + bc - abc + d - ad + bd - abd - cd + acd - bcd + abcd)
	contrast_BCD = np.sum(-one - a + b + ab + c + ac - bc - abc + d + ad - bd - abd - cd - acd + bcd + abcd)
	contrast_ABCD = np.sum(one - a - b + ab - c + ac + bc - abc - d + ad + bd - abd + cd - acd - bcd + abcd)
	contrasts_all = np.array([contrast_A, contrast_B, contrast_AB, contrast_C, contrast_AC, contrast_BC, contrast_ABC,
                         contrast_D, contrast_AD, contrast_BD, contrast_ABD, contrast_CD, contrast_ACD, contrast_BCD, contrast_ABCD])
if(k >= 5):
	df_index=['A', 'B', 'AB', 'C', 'AC', 'BC', 'ABC', 'D', 'AD', 'BD', 'ABD', 'CD', 'ACD', 'BCD', 'ABCD', 'E', 'AE', 'BE', 'ABE',
	'CE', 'ACE', 'BCE', 'ABCE','DE', 'ADE', 'BDE', 'ABDE', 'CDE', 'ACDE', 'BCDE', 'ABCDE', 'Error', 'Total']
	e 	= response_var[response_var['code'] == 'E'].loc[:,rv[1]].to_numpy()
	ae 	= response_var[response_var['code'] == 'AE'].loc[:,rv[1]].to_numpy()
	be 	= response_var[response_var['code'] == 'BE'].loc[:,rv[1]].to_numpy()
	abe = response_var[response_var['code'] == 'ABE'].loc[:,rv[1]].to_numpy()
	ce 	= response_var[response_var['code'] == 'CE'].loc[:,rv[1]].to_numpy()
	ace = response_var[response_var['code'] ==  'ACE'].loc[:,rv[1]].to_numpy()
	bce = response_var[response_var['code'] == 'BCE'].loc[:,rv[1]].to_numpy()
	abce = response_var[response_var['code'] == 'ABCE'].loc[:,rv[1]].to_numpy()
	de 	= response_var[response_var['code'] == 'DE'].loc[:,rv[1]].to_numpy()
	ade = response_var[response_var['code'] == 'ADE'].loc[:,rv[1]].to_numpy()
	bde = response_var[response_var['code'] == 'BDE'].loc[:,rv[1]].to_numpy()
	abde = response_var[response_var['code'] == 'ABDE'].loc[:,rv[1]].to_numpy()
	cde = response_var[response_var['code'] == 'CDE'].loc[:,rv[1]].to_numpy()
	acde = response_var[response_var['code'] == 'ACDE'].loc[:,rv[1]].to_numpy()
	bcde = response_var[response_var['code'] == 'BCDE'].loc[:,rv[1]].to_numpy()
	abcde = response_var[response_var['code'] == 'ABCDE'].loc[:,rv[1]].to_numpy()
	means_all = np.array([np.mean(a), np.mean(b), np.mean(ab), np.mean(c), np.mean(ac), np.mean(bc), np.mean(abc), np.mean(d),
							np.mean(ad), np.mean(bd), np.mean(abd), np.mean(cd), np.mean(acd), np.mean(bcd), np.mean(abcd),np.mean(e),
							np.mean(ae),np.mean(be),np.mean(abe),np.mean(ce),np.mean(ace),np.mean(bce),np.mean(abce),np.mean(de),np.mean(ade),
							np.mean(bde),np.mean(abde),np.mean(cde),np.mean(acde),np.mean(bcde),np.mean(abcde)])
	total = np.array([one, a, b, ab, c, ac, bc, abc, d, ad, bd, abd, cd, acd, bcd, abcd,
					e,ae,be,abe,ce,ace,bce,abce,de,ade,bde,abde,cde,acde,bcde,abcde])
	contrast_A = np.sum(-one + a  - b  + ab  - c  + ac  - bc  + abc  - d  + ad  - bd  + abd  - cd  + acd  - bcd  + abcd
						- e  + ae - be + abe - ce + ace - bce + abce - de + ade - bde + abde - cde + acde - bcde + abcde)
	contrast_B = np.sum(-one - a  + b  + ab  - c  - ac  + bc  + abc  - d  - ad  + bd  + abd  - cd  - acd  + bcd  + abcd
						- e  - ae + be + abe - ce - ace + bce + abce - de - ade + bde + abde - cde - acde + bcde + abcde)
	contrast_AB = np.sum(one - a  - b  + ab  + c  - ac  - bc  + abc  + d  - ad  - bd  + abd  + cd  - acd  - bcd  + abcd
						+ e  - ae - be + abe + ce - ace - bce + abce + de - ade - bde + abde + cde - acde - bcde + abcde)
	contrast_C = np.sum(-one - a  - b  - ab  + c  + ac  + bc  + abc  - d  - ad  - bd  - abd  + cd  + acd  + bcd  + abcd
						- e  - ae - be - abe + ce + ace + bce + abce - de - ade - bde - abde + cde + acde + bcde + abcde)
	contrast_AC = np.sum(one - a  + b  - ab  - c  + ac  - bc  + abc  + d  - ad  + bd  - abd  - cd  + acd  - bcd  + abcd
						+ e  - ae + be - abe - ce + ace - bce + abce + de - ade + bde - abde - cde + acde - bcde + abcde)
	contrast_BC = np.sum(one + a  - b  - ab  - c  - ac  + bc  + abc  + d  + ad  - bd  - abd  - cd  - acd  + bcd  + abcd
						+ e  + ae - be - abe - ce - ace + bce + abce + de + ade - bde - abde - cde - acde + bcde + abcde)
	contrast_ABC= np.sum(-one + a  + b  - ab  + c  - ac  - bc  + abc  - d  + ad  + bd  - abd  + cd  - acd  - bcd  + abcd
						 - e  + ae + be - abe + ce - ace - bce + abce - de + ade + bde - abde + cde - acde - bcde + abcde)
	contrast_D =  np.sum(-one - a  - b  - ab  - c  - ac  - bc  - abc  + d  + ad  + bd  + abd  + cd  + acd  + bcd  + abcd
						 - e  - ae - be - abe - ce - ace - bce - abce + de + ade + bde + abde + cde + acde + bcde + abcde)
	contrast_AD=  np.sum(one - a  + b  - ab  + c  - ac  + bc  - abc  - d  + ad  - bd  + abd  - cd  + acd  - bcd  + abcd
						+ e  - ae + be - abe + ce - ace + bce - abce - de + ade - bde + abde - cde + acde - bcde + abcde)
	contrast_BD = np.sum(one + a  - b  - ab  + c  + ac  - bc  - abc  - d  - ad  + bd  + abd  - cd  - acd  + bcd  + abcd
						+ e  + ae - be - abe + ce + ace - bce - abce - de - ade + bde + abde - cde - acde + bcde + abcde)
	contrast_ABD= np.sum(-one + a + b  - ab  - c  + ac  + bc  - abc  + d  - ad  - bd  + abd  + cd  - acd  - bcd  + abcd
						 - e + ae + be - abe - ce + ace + bce - abce + de - ade - bde + abde + cde - acde - bcde + abcde)
	contrast_CD = np.sum(one + a  + b  + ab  - c  - ac  - bc  - abc  - d  - ad  - bd  - abd  + cd  + acd  + bcd  + abcd
						+ e  + ae + be + abe - ce - ace - bce - abce - de - ade - bde - abde + cde + acde + bcde + abcde)
	contrast_ACD = np.sum(-one + a  - b  + ab  + c  - ac  + bc  - abc  + d  - ad  + bd  - abd  - cd  + acd  - bcd  + abcd
						  - e  + ae - be + abe + ce - ace + bce - abce + de - ade + bde - abde - cde + acde - bcde + abcde)
	contrast_BCD = np.sum(-one - a  + b  + ab  + c  + ac  - bc  - abc  + d  + ad  - bd  - abd  - cd  - acd  + bcd  + abcd
						  - e  - ae + be + abe + ce + ace - bce - abce + de + ade - bde - abde - cde - acde + bcde + abcde)
	contrast_ABCD = np.sum(one - a  - b  + ab  - c  + ac  + bc  - abc  - d  + ad  + bd  - abd  + cd  - acd  - bcd  + abcd
						  + e  - ae - be + abe - ce + ace + bce - abce - de + ade + bde - abde + cde - acde - bcde + abcde)
	contrast_E = np.sum(-one - a  - b  - ab  - c  - ac  - bc  - abc  - d  - ad  - bd  - abd  - cd  - acd  - bcd  - abcd
						+ e  + ae + be + abe + ce + ace + bce + abce + de + ade + bde + abde + cde + acde + bcde + abcde)
	contrast_AE = np.sum(one - a  + b  - ab  + c  - ac  + bc  - abc  + d  - ad  + bd  - abd  + cd  - acd  + bcd  - abcd
					    - e  + ae - be + abe - ce + ace - bce + abce - de + ade - bde + abde - cde + acde - bcde + abcde)
	contrast_BE= np.sum(one + a  - b  - ab  + c  + ac  - bc  - abc  + d  + ad  - bd  - abd  + cd  + acd  - bcd  - abcd
						- e - ae + be + abe - ce - ace + bce + abce - de - ade + bde + abde - cde - acde + bcde + abcde)
	contrast_ABE= np.sum(-one + a  + b  - ab  - c  + ac  + bc  - abc  - d  + ad  + bd  - abd  - cd  + acd  + bcd  - abcd
						 + e  - ae - be + abe + ce - ace - bce + abce + de - ade - bde + abde + cde - acde - bcde + abcde)
	contrast_CE= np.sum(one + a  + b  + ab  - c  - ac  - bc  - abc  + d  + ad  + bd  + abd  - cd  - acd  - bcd  - abcd
						- e - ae - be - abe + ce + ace + bce + abce - de - ade - bde - abde + cde + acde + bcde + abcde)
	contrast_ACE= np.sum(-one + a  - b  + ab  + c  - ac  + bc  - abc  - d  + ad  - bd  + abd  + cd  - acd  + bcd  - abcd
						 + e  - ae + be - abe - ce + ace - bce + abce + de - ade + bde - abde - cde + acde - bcde + abcde)
	contrast_BCE= np.sum(-one - a  + b  + ab  + c  + ac  - bc  - abc  - d  - ad  + bd  + abd  + cd  + acd  - bcd  - abcd
					  	 + e  + ae - be - abe - ce - ace + bce + abce + de + ade - bde - abde - cde - acde + bcde + abcde)
	contrast_ABCE= np.sum(one - a  - b  + ab  - c  + ac  + bc  - abc  + d  - ad  - bd  + abd  - cd  + acd  + bcd  - abcd
						  - e + ae + be - abe + ce - ace - bce + abce - de + ade + bde - abde + cde - acde - bcde + abcde)
	contrast_DE= np.sum(one + a  + b  + ab  + c  + ac  + bc  + abc  - d  - ad  - bd  - abd  - cd  - acd  - bcd  - abcd
						- e - ae - be - abe - ce - ace - bce - abce + de + ade + bde + abde + cde + acde + bcde + abcde)
	contrast_ADE= np.sum(-one + a  - b  + ab  - c  + ac  - bc  + abc  + d  - ad  + bd  - abd  + cd  - acd  + bcd  - abcd
						 + e  - ae + be - abe + ce - ace + bce - abce - de + ade - bde + abde - cde + acde - bcde + abcde)
	contrast_BDE= np.sum(-one - a  + b  + ab  - c  - ac  + bc  + abc  + d  + ad  - bd  - abd  + cd  + acd  - bcd  - abcd
						 + e  + ae - be - abe + ce + ace - bce - abce - de - ade + bde + abde - cde - acde + bcde + abcde)
	contrast_ABDE= np.sum(one - a  - b  + ab  + c  - ac  - bc  + abc  - d  + ad  + bd  - abd  - cd  + acd  + bcd  - abcd
						 - e  + ae + be - abe - ce + ace + bce - abce + de - ade - bde + abde + cde - acde - bcde + abcde)
	contrast_CDE= np.sum(-one - a  - b  - ab  + c  + ac  + bc  + abc  + d  + ad  + bd  + abd  - cd  - acd  - bcd  - abcd
						 + e  + ae + be + abe - ce - ace - bce - abce - de - ade - bde - abde + cde + acde + bcde + abcde)
	contrast_ACDE= np.sum(one - a  + b  - ab  - c  + ac  - bc  + abc  - d  + ad  - bd  + abd  + cd  - acd  + bcd  - abcd
						 - e  + ae - be + abe + ce - ace + bce - abce + de - ade + bde - abde - cde + acde - bcde + abcde)
	contrast_BCDE= np.sum(one + a  - b  - ab  - c  - ac  + bc  + abc  - d  - ad  + bd  + abd  + cd  + acd  - bcd  - abcd
						  - e - ae + be + abe + ce + ace - bce - abce + de + ade - bde - abde - cde - acde + bcde + abcde)
	contrast_ABCDE= np.sum(-one + a  + b  - ab  + c  - ac  - bc  + abc  + d  - ad  - bd  + abd  - cd  + acd  + bcd  - abcd
						   + e  - ae - be + abe - ce + ace + bce - abce - de + ade + bde - abde + cde - acde - bcde + abcde)

	contrasts_all = np.array([contrast_A, contrast_B, contrast_AB, contrast_C, contrast_AC, contrast_BC, contrast_ABC,
							 contrast_D, contrast_AD, contrast_BD, contrast_ABD, contrast_CD, contrast_ACD, contrast_BCD, contrast_ABCD,
							 contrast_E, contrast_AE, contrast_BE, contrast_ABE, contrast_CE, contrast_ACE, contrast_BCE, contrast_ABCE,
							 contrast_DE, contrast_ADE, contrast_BDE, contrast_ABDE, contrast_CDE, contrast_ACDE, contrast_BCDE, contrast_ABCDE])


# Sum Squares
num_effects = np.power(2,k)-1
num_elements = num_effects+2
sum_squares = np.ones(num_elements) #All effects plus error and total
for i in range(num_effects):
	sum_squares[i] = np.square(contrasts_all[i])/(n*np.power(2,k))
total_mean = np.mean(total)
SST = np.sum(np.square(total - total_mean))
SSE = SST - np.sum(sum_squares[0:num_effects])
sum_squares[num_effects] = SSE
sum_squares[num_effects+1] = SST

#Degrees of Freedom
DF = np.ones(num_elements)
DF[num_effects] = np.power(2,k)*(n-1) # Error DoF
DF[num_effects+1] = n*np.power(2,k)-1 # Total DoF

#Mean Squares
mean_squares = np.ones(sum_squares.size)
for i in range(num_elements):
    mean_squares[i] = sum_squares[i]/DF[i]
MSE = mean_squares[num_effects]

#F-values
f_vals = np.ones(num_elements)
f_vals[num_effects:] = -1
f_crits = np.ones(num_elements)
f_crits[num_effects:] = -1

#P-values
p_vals = np.ones(num_elements)
p_vals[num_effects:] = -1

#Effect Estimates
effects = np.ones(num_elements)
effects[num_effects:] = -1

#Response variable averages
means = np.ones(num_elements)
means[num_effects:] = -1

#Build datafile
for i in range(num_effects):
    F0 = mean_squares[i]/MSE
    f_vals[i] = F0
    f_crits[i] = stats.f.ppf(1-alpha,DF[i],DF[num_effects])
    p_vals[i] = 1 - stats.f.cdf(F0, DF[i],DF[num_effects])
    effects[i] = contrasts_all[i]/(n*np.power(2,k-1))
    means[i] = means_all[i]

anova_df_numpy = np.array([means, effects, sum_squares, DF, mean_squares, f_vals, f_crits, p_vals])
anova_df_pandas = pd.DataFrame(data=anova_df_numpy.T, index=df_index, columns=['Sample Mean','Effect Est.','Sum of Squares', 'df', 'Mean Square', 'F0', 'F Threshold', 'p-value'])
anova_df_pandas = anova_df_pandas.replace(to_replace=-1,value='')

#The deprecated function. Changes p-value to float64 so it can be rounded properly
anova_df_pandas['p-value']= anova_df_pandas['p-value'].convert_objects(convert_numeric=True)
print("Unoptimized Mean: " + str(np.mean(one)))
print(anova_df_pandas.round(5))

##Significant Factors
significant_factors = anova_df_pandas[(anova_df_pandas['p-value'] < alpha)].round(5)

#Ideal candidates are less then the unoptimized mean...
candidiate_factors = significant_factors[(significant_factors['Sample Mean'] < np.mean(one))].sort_values(by=['Sample Mean'])

longest = ""

#Print all the significant factors at chosen p-value
if significant_factors.empty == False:
	anova_df_pandas[(anova_df_pandas['p-value'] < alpha)].to_csv("results/anova/" + sys.argv[6]+"-"+input_csv_parse[2]+"-"+rv[0]+"-"+rv[1]+"-anova-significant.csv")

#Print them all to another file 
anova_df_pandas.to_csv("results/anova/" + sys.argv[6]+"-"+ input_csv_parse[2]+"-"+rv[0]+"-"+rv[1]+"-anova-all.csv")

#If I have significant candidate factors with sample mean < unoptimized mean: 
if candidiate_factors.empty == False:
	print("\nSignificant Factors (alpha = " + str(alpha) + ")")
	print(significant_factors.sort_values(by=['Sample Mean']))
	#candidiate_factors_index = candidiate_factors[(candidiate_factors['Sample Mean'] < np.mean(one))].sort_values(by=['Sample Mean']).index.array
	candidiate_factors_index = candidiate_factors.sort_values(by=['Sample Mean']).index.array

	for x in candidiate_factors_index:
		if len(x) > len(longest):
			longest = x

	print("\n!!--Statistically Significant Effects--!! ")
	all = ""
	for y in candidiate_factors_index:
		all = all + y + ","
	print("Lowest observed mean (Target to Beat)")
	print(int(significant_factors['Sample Mean'].min()))
	print("Effects")

#If all my significant candidate factors actually have a worse sample mean: 
else:
	print("\n ***No statistically significant effects with sample mean < unoptimized mean***\n")
	candidiate_factors_index = anova_df_pandas[(anova_df_pandas['Sample Mean'] < np.mean(one))].sort_values(by=['Sample Mean']).index.array

	all = ""
	for y in candidiate_factors_index:
		all = all + y + ","

	if len(all) == 0:

		print("Unoptimized Mean")
		print(str(np.mean(one)))
		print("***ALL effects attempted have sample mean > unoptimized mean***")
		print("NONE")
		exit()

	#Take the factor combo with the best sample mean and keep trying
	print("Lowest observed sample mean (Target to Beat)")
	print(int(anova_df_pandas[(anova_df_pandas['Sample Mean'] < np.mean(one))]['Sample Mean'].min()))
	print("Next best guesses (produced a sample mean lower than unoptimized)")

if len(all) == 0:
	print("NONE - ERROR") #I shouldn't get here...
else:
	print(all.rstrip(','))

#Normplot of effects
if len(sys.argv) == 7:
	fig = plt.figure(figsize=(6,4))
	probscale.probplot(effects,plottype='prob',probax='y',problabel='Standard Normal Probabilities',bestfit=True)
	plt.xlabel("Normal Probability Plot of Effect Estimates")
	plt.title(rv[0] +" - " + rv[1] + " [" + sys.argv[6] +"]")
	plt.tight_layout()
	plt.savefig("results/anova/"+sys.argv[6]+"-"+input_csv_parse[2]+"-"+rv[0]+"-"+rv[1]+"-anova-normplot.png")
