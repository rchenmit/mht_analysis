\name{importDefaults}
\alias{importDefaults}
\alias{.importDefaults}
\title{ Import Global Default Argument Values }
\description{
Use globally specified defaults, if set,
in place of formally specified default
argument values.  Allows user to specify
function defaults different than formally
supplied values, e.g. to change poorly
performing defaults, or satisfy a different
preference.
}
\usage{
importDefaults(calling.fun)
}
\arguments{
  \item{calling.fun}{ name of function to act upon }
}
\details{
Placed immediately after the function declaration,
a call to \code{importDefaults} checks the
user's environment for globally specified
default values for the called function.
These defaults can be specified by the user with a
call to \code{setDefaults}, and will override
any default formal parameters, in effect
replacing the original defaults with user
supplied values instead.

If a function has \emph{not} been written with
\code{importDefaults} (most \R functions, so far\ldots),
it is possible to
simply call \code{useDefaults} to achieve
the same results. As of version 1.1-0, simply calling
\code{setDefaults} will call \code{useDefaults}
internally, removing the need to explicitly
call. See the related help page.

Any values specified by the user in a
in the parent function
(that is, the function containing
\code{importDefaults}) will override the values
set in the global default environment.
}
\value{
Used for its side-effects, a call to \code{importDefaults}
loads all non-NULL default values specified by the user
into the current function's environment, effectively changing the
default values passed in the parent function call.

\code{importDefaults} values, like formally defined
defaults in the function definition, take lower
precedence than arguments specified by the user in
the function call.

An alias to \code{importDefaults}, \code{.importDefaults}
is the actual function added when \code{useDefaults} is
called on a function. The naming convention is designed to
facilitate setting and unsetting, and should \emph{NOT} be
used by the function developer. Please use only \code{importDefaults}
}
\author{ Jeffrey A. Ryan }
\note{ 
It is important to note that when a function
implements \code{importDefaults}, non-named
arguments \emph{may} be ignored if a global
Default has been set (i.e. not NULL).

If this is the case, simply name the arguments
in the calling function.

This \emph{should} also work for functions
retrieving formal parameter values
from \code{options}, as
it assigns a value to the parameter in
a way that looks like it was passed in
the function call. So any check on \code{options}
would presumably disregard \code{importDefaults}
values if an argument
was passed to the function (what \code{useDefaults}
does)
}
\seealso{ \code{\link{useDefaults}},\code{\link{setDefaults}} }
\examples{
my.fun <- function(x=3)
{
  importDefaults('my.fun')
  x ^ 2
}

my.fun()        #returns 9

setDefaults(my.fun,x=10)
my.fun()        #returns 100
my.fun(x=4)     #returns 16

getDefaults(my.fun)
formals(my.fun)
unsetDefaults(my.fun,confirm=FALSE)
getDefaults(my.fun)

my.fun()        #returns 9
}
\keyword{ utilities }
