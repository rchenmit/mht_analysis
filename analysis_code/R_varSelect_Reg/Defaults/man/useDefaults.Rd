\name{useDefaults}
\alias{useDefaults}
\alias{unDefaults}
\title{ Enable and Disable Global Defaults By Function }
\description{
Allows for the use of globally managed default
values for formal function arguments. Adds
the ability to pre-specify a value for any formal
argument as if it were specified in the function call.
} 
\usage{
useDefaults(name)
unDefaults(name)
}
\arguments{
  \item{name}{ name of function, quoted or unquoted }
}
\details{
These functions are called automatically during
calls to \code{setDefaults} and \code{unsetDefaults}, though
they may be called by the user as well.

Defaults are set inside the named function with
a call to \code{importDefaults}.  This may be hard
coded into the function by the author, or may be
dynamically added with a call to \code{useDefaults}.

Internally, a new call to \code{importDefaults}
is added before the body of the function \code{name}.
This is added in the first occurence of the specified
function encountered in the search path.
That is, if there are two function objects, the first
encountered will be modified. The modification
takes place in the environment of
the original function, so namespaces are retained.

\code{useDefaults} replaces all formal functional
arguments with all non-NULL globally specified ones
after first checking that these global defaults have
not been overridden with new values in the function 
call.

The order of lookup is as follows, with the lookup
halted once a specified value is found:

\enumerate{
    \item{}{1. Check for arguments specified 
       in the actual call}

    \item{}{2. Check for arguments specified by setDefaults}

    \item{}{3. Use original function defaults. (if any)}
}

Setting default values is accompished via
\code{setDefaults}, with the values being written
to \R's \code{options} list as a named list set
to the function's name appended with a .Default,
all managed automatically.  It is possible to view
and delete all defaults with the functions
\code{getDefaults} and \code{unsetDefaults}, 
respectively. All \R objects can be saved to
the Defaults list, with the exception of \code{NULL},
as this removes the argument from the Defaults list instead.

To return a function enabled by \code{useDefaults}
to its original state, call \code{unDefaults}.
Conceptually this is similar to \code{debug} and
\code{undebug}, though implemented entirely in \R.
The current implementation borrows from the R function
\code{trace} and more directly, Mark V. Bravington's \code{mtrace}.
}
\value{
None. Called for its side effect of enabling
or disabling the Defaults mechanism. The only
use visible side-effect is the modified function
body.
}
\author{ Jeffrey A. Ryan }
\references{
Mark V. Bravington (2005) \emph{ debug: MVB's debugger for R },
R package version 1.1.0
}
\note{
The underlying \code{importDefaults} mechanism relies on
the calling function to have the same name as function in which
it is located.
This is the case in almost all circumstances, excepting one -
when called as the passed FUN object in an lapply or similar
call, as the calling function will then simply be
\sQuote{FUN} or something similar.
In these circumstances the function will behave as
if \code{useDefaults} had \emph{not} been called on it, i.e.
no check of global Defaults will be occur. If Defaults behavior
is desired, simply create an anonymous function wrapper to
the function in question, as this will then resolve correctly.

A special thanks to John Chambers and Dirk Eddelbuettel
for providing guidance on handling functions using
namespaces, as well as pointing out the original
mishandling of namespace issues.
}
\seealso{ \code{\link{importDefaults}},
          \code{\link{setDefaults}},
          \code{\link{formals}},
          \code{\link{body}},
          \code{\link{as.function}}
}
\examples{
my.fun <- function(x=2,y=1) { x ^ y }
my.fun()            #returns 2
my.fun(x=2,y=10)    #returns 1024

setDefaults(my.fun,x=2,y=3)
useDefaults(my.fun)
my.fun

my.fun()            #returns 8
my.fun(y=10)        #returns 1024
my.fun(x=2,y=10)    #returns 1024

unDefaults(my.fun)
my.fun
my.fun()            #returns 2

getDefaults(my.fun)
unsetDefaults(my.fun,confirm=FALSE)  
getDefaults(my.fun)
}
\keyword{ utilities }
