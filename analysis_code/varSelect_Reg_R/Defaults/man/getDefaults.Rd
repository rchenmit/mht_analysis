\name{getDefaults}
\alias{getDefaults}
\title{ Show Global Defaults List By Function }
\description{
Show global Default list by function or
specified argument values by function.
} 
\usage{
getDefaults(name=NULL, arg = NULL)
}
\arguments{
  \item{name}{ name of function, quoted or unquoted }
  \item{arg}{ values to retrieve } 
}
\details{
A list of function names currently with
Defaults set can be seen by calling \code{getDefaults()}
with no arguments.

This \emph{does not} imply that the returned function
names are currently set to accept defaults (via
\code{useDefaults} or hard-coded with
\code{importDefaults}, rather that they have been
set up to store user Defaults.

All values can be viewed less elegantly by a call
to \code{getOption(name_of_function.Default)}
}
\value{
\code{getDefaults} returns a named list of defaults
and associated values, similar to \code{formals}, only
returning \code{setDefaults} set values for the
\code{name} function. Single arguments need
not be quoted, multiples must be as a character
vector. Calling \code{getDefaults()} without
arguments results in a character vector of
all functions currently having Defaults set
(by \code{setDefaults})
}
\author{ Jeffrey A. Ryan }
\seealso{
          \code{\link{setDefaults}},
          \code{\link{useDefaults}},
          \code{\link{options}}
}
\examples{
setDefaults(lm,na.action='na.exclude',singular.ok=TRUE)

getDefaults()
getDefaults(lm)

unsetDefaults(lm,confirm=FALSE)  
getDefaults(lm)



my.fun <- function(x=2,y=1) { x ^ y } 
my.fun()                #returns 2 
my.fun(x=2,y=10)        #returns 1024 

setDefaults(my.fun,x=2,y=3) 
useDefaults(my.fun) 
my.fun 

my.fun()                #returns 8 
my.fun(y=10)            #returns 1024 
my.fun(x=2,y=10)        #returns 1024 

unDefaults(my.fun) 
my.fun 
my.fun()                #returns 2 

getDefaults(my.fun) 
unsetDefaults(my.fun,confirm=FALSE) 
getDefaults(my.fun) 
}
\keyword{ utilities }
