
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

