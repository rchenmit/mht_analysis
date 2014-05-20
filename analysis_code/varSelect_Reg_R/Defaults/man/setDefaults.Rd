\name{setDefaults}
\alias{setDefaults}
\alias{unsetDefaults}
\title{ Create Global Defaults List By Function }
\description{
Create Defaults to be used
in place of a function's formal
argumenent values.

In conjuction with \code{useDefaults}, or
functions already supporting
\code{importDefaults}, to allow for
user override of formal arguments without specifying
in the function call.

See \code{useDefaults} for the details of
this process.
} 
\usage{
setDefaults(.name,...)
unsetDefaults(name, confirm=TRUE)
}
\arguments{
  \item{.name}{ name of function, quoted or unquoted }
  \item{name}{ name of function, quoted or unquoted }
  \item{\dots}{ name=value default pairs }
  \item{confirm}{ prompt before unsetting defaults }
}
\details{
setDefaults is a wrapper to
\R \code{options}, allowing the user
to specify any name=value pair that
a function has in it's formal arguments.

Calling \code{setDefaults} on an object
that previously could not process Defaults will
automatically enable defaults via an internal
call to \code{useDefaults}.

Only formal name=value pairs specified will be updated.
Values do not have to be respecified in subsequent calls
to \code{setDefaults}, so it is possible to add
new defaults one at a time for each function, without
having to retype all previous values. Assigning
NULL to any argument will remove the argument from the
Defaults list.

When a function is set to use these Defaults
(using \code{useDefaults}, \code{setDefaults}, or hard-coded
to use the \pkg{Defaults} package) 
all non-NULL values set by \code{setDefaults}
will effectively replace all formally
specified function defaults.

At present it is not possible to specify NULL
as a replacement for a non-NULL default, as the
process interprets NULL values as being not set, and
will simply use the value specified formally
in the function. If NULL is what is desired, it
is necessary to include this in the function call
itself.

Any arguments included in the actual function
call will take precedence over \code{setDefaults}
values, as well as the standard formal function
values. This conforms to the current user
experience in \R. 

\code{unsetDefaults} does exactly what it says.
}
\value{
None. Called for it's side effect of setting
a list of Default arguments by function.
}
\author{ Jeffrey A. Ryan }
\note{
Like \code{options}, settings are \emph{NOT}
kept across sessions.

Currently, it is \emph{NOT} possible to pass
values for \dots arguments, only formally specified
arguments in the original function definition.

If it is desired to pass additional arguments,
or more specifically have new defaults, to
subsequent methods/calls, a seperate \code{setDefaults}
\code{useDefaults} series is required.

\code{unsetDefaults} removes the \emph{all} entries from
the \code{options} lists for the specified function, and
then calls \code{unDefaults}. To remove single function Default
values simply set the name of the argument to
NULL in \code{setDefaults}
}
\seealso{ 
          \code{\link{options}},
          \code{\link{getDefaults}},
          \code{\link{useDefaults}},
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
setDefaults(my.fun,x=NULL)  #removes the value for x, leaving just y
unsetDefaults(my.fun,confirm=FALSE)  
getDefaults(my.fun)
}
\keyword{ utilities }
