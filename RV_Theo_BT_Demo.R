library(scales)

plot_theo <- function(bid, ask, method) {
  n = length(bid)
  x = 1:(n*2)
  y_bid = rep(bid, each=2)
  y_ask = rep(ask, each=2)
  s = seq(1, 2*n-1, 2)
  
  plot(x, x, main=paste('Theo Update (', method, ')', sep=''), ylim=c(min(y_bid), max(y_ask)), xlab='Time Index', ylab='Price', type='n')
  segments(x[s], y_bid[s], x[s+1], y_bid[s+1], col='blue')
  segments(x[s], y_ask[s], x[s+1], y_ask[s+1], col='red')
  if(method=='LongGamma') {
    theo = rep(0, n)
    theo[1] = bid[1]
    for(i in 2:n) {
      theo[i] = (bid[i]>theo[i-1]) * bid[i] + (ask[i]<theo[i-1]) * ask[i] + 
                  (bid[i]<=theo[i-1] & ask[i]>=theo[i-1]) * theo[i-1]
    }
  }
  if(method=='ShortGamma') {
    theo = rep(0, n)
    theo[1] = bid[1]
    for(i in 2:n) {
      theo[i] = (bid[i]>theo[i-1]) * ask[i] + (ask[i]<theo[i-1]) * bid[i] + 
        (bid[i]<=theo[i-1] & ask[i]>=theo[i-1]) * theo[i-1]
    }
  }
  y_theo = rep(theo, each=2)
  segments(x[s], y_theo[s], x[s+1], y_theo[s+1], col='darkgreen')
  arrows(x[s+1]+0.2, y_theo[s+1], x[s+2]-0.2, y_theo[s+2], col='black', length='0.05')
  legend("topleft", legend = c('theo', 'ask', 'bid'), col = c('darkgreen', 'red', 'blue'), cex=0.4, bty='n', lty=1)
}

n = 30
bid = 12 + cumsum(0.1*c(sample(c(-2,-1,1,2), n, replace=TRUE)))
ask = bid + 0.1*c(sample(c(1,2), n, replace=TRUE))
par(mfrow=c(2,1))
plot_theo(bid, ask, 'LongGamma')
plot_theo(bid, ask, 'ShortGamma')

