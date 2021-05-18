# preliminar ####
rm(list=ls())

librerias <- c('stringr','dplyr','ggplot2','ggpubr','knitr','tidyverse',
               'reshape2','tinytex','gt','haven',
               'dagitty','ellipse','mvtnorm','MASS','splines','gtools',
               'rethinking','rstan','coda','runjags','rjags','loo')
sapply(librerias, require, character.only=T)
# sapply(librerias, install.packages, character.only=T)

setwd('~/Desktop/project_europa')


# data ####

## load ####
file_dir = '/home/jriveraespejo/Desktop/project_europa/data/final/8_NLPdata.csv'
wordcloud = read.csv(file_dir)
# str(wordcloud)
# dim(wordcloud)


## prepare ####

# train set
N = nrow(wordcloud)
idx = sample(1:N, size=round(N*0.9))
train = rep(FALSE, N)
train[idx] = TRUE
# sum(train)

data_list = list(N = nrow(wordcloud[train,]),
                 K = ncol(wordcloud)-1, 
                 G = wordcloud$G[train],
                 W = as.matrix(wordcloud[train,-c(251:252)]) )
# str(data_list)



# model ####

mcmc_code <- "
data {
    int N;
    int K;
    int G[N];
    matrix[N, K] W;
}
parameters {
    vector[K] b;
}
model {
    vector[N] v; // linear predictor
    vector[N] p; // probability
    
    // priors
    // LASSO prior (highly regularizing), 
    b ~ double_exponential(0, 0.2);
    
    //# // highly regularizing prior (not LASSO, not multilevel)
    //# b ~ normal(0, 0.2); 
    
    // model
    v = W * b;
    p = inv_logit(v);
    G ~ bernoulli(p);
}
generated quantities{
    vector[N] v; // linear predictor
    vector[N] p; // probability
    vector[N] log_lik; // log-likelihood
    
    // model
    v = W * b;
    p = inv_logit(v);
    
    for(i in 1:N){
      log_lik[i] = bernoulli_lpmf(G[i] | p[i]);
    }
}
"
save_code = file.path('notebooks', "wordcloud_model.stan" )
writeLines( mcmc_code, con=save_code)
mcmc_model <- stan( file=save_code, data=data_list, chains=4, cores=4)




# results ####
results = precis( mcmc_model, dept=2 )
idx_names = str_detect( rownames(results), '^b')
results = results[idx_names, ]
rownames(results) = names(wordcloud)[-c(251:252)]


# parameters
round( head( results[order(results$mean, decreasing = F),], 20) , 2 )
round( head( results[order(results$mean, decreasing = T),], 20), 2 )


# fit
WAIC(mcmc_model)
PSIS(mcmc_model) # some k pareto values indicate outliers


# outliers
PSIS_res = PSIS(mcmc_model, pointwise=T)
head( PSIS_res[ order(PSIS_res$k, decreasing = T), ], 10)

idx_outlier = c(385, 388, 389, 391, 396, 397)
company_names = wordcloud[train, 'Name']
company_names[idx_outlier]
rowSums( data_list$W[idx_outlier,] )
# they are outliers because there is no info about their industry




# assessing chains ####

idx = paste0('b[',1:12,']')

## stationarity and convergence ####

par(mfrow=c(4,3))
traceplot_ulam(mcmc_model, pars=idx) 
# stationarity, and convergence
par(mfrow=c(1,1))


## good mixing ####

### trankplots ####

par(mfrow=c(4,3))
trankplot(mcmc_model, pars=idx) 
# good mixing
par(mfrow=c(1,1))

### autocorrelation ####
acf_plot = function(mcmc_object, pars){
  
  # mcmc_object = mcmc_model
  n_pars = length(pars)
  
  if(class(mcmc_object) == 'stanfit'){
    sim_object = mcmc_object@sim[[1]][[1]]
    
    for(p in 1:n_pars){
      acf(sim_object[pars[p]][[1]], main='', xlab='', 
          mar = c(0, 0, 0, 0) )
      mtext( pars[p], side=3, adj=0, cex=1)
    }
    
  } else{
    sim_object = mcmc_object$mcmc[[1]]
    
    for(p in 1:n_pars){
      acf(sim_object[colnames(sim_object) == pars[p]], main='', xlab='',
          mar = c(0, 0, 0, 0) )
      mtext( pars[p], side=3, adj=0, cex=1)
    }
    
  }
  
}

par(mfrow=c(4,3))
acf_plot(mcmc_model, pars=idx)
par(mfrow=c(1,1))



# posterior predictive ####
G_test = wordcloud$G[!train]
W_test = as.matrix(wordcloud[!train,-251])

post = extract.samples(mcmc_model)
post = post$b
pars_mu = apply(post, 2, mean)
pars_CI = apply(post, 2, PI, 0.95)

v = W_test %*% pars_mu
p = as.integer( inv_logit(v) >= 0.5)
table(G_test, p)

# v = W_test %*% t(pars_CI)
# p = apply( inv_logit(v) >= 0.5, 2, as.integer)
# table(G_test, p[,1])
# table(G_test, p[,2])
