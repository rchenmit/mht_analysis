library(Defaults)
a <- function(x=0) {
  importDefaults(calling.fun='a')
  x
}
b <- function(x=0) {
  x
}

test.equality <- function(x,y) {
  if(identical(x,y)) {
    cat("OK\n")
    return(FALSE)
  } else {
    cat("failed\n")
    return(TRUE)
  }
}

cat("Testing importDefaults:\n\n")

setDefaults(a,x=1)
cat("testing x=1 default:\t\t\t")
test.equality(a(),1)

setDefaults(a,x=1:10)
cat("testing x=1:10 default:\t\t\t")
test.equality(a(),1:10)

setDefaults(a,x=letters)
cat("testing x=letters default:\t\t")
test.equality(a(),letters)

setDefaults(a,x=c('a','b'))
cat("testing x=c('a','b') default:\t\t")
test.equality(a(),c('a','b'))

setDefaults(a,x=a)
cat("testing x=a default:\t\t\t")
test.equality(a(),a)

setDefaults(a,x="a")
cat("testing x='a' default:\t\t\t")
test.equality(a(),"a")

setDefaults(a,x=NULL)
cat("testing x=NULL default:\t\t\t")
test.equality(a(),0)

setDefaults(a,x=list(a=1,b=2))
cat("testing x=list(a=1,b=2) default:\t")
test.equality(a(),list(a=1,b=2))


cat("\n\n\nuseDefaults(b)...\n\n")
useDefaults(b)
cat("Testing useDefaults:\n\n")

setDefaults(b,x=1)
cat("testing x=1 default:\t\t\t")
test.equality(b(),1)

setDefaults(b,x=1:10)
cat("testing x=1:10 default:\t\t\t")
test.equality(b(),1:10)

setDefaults(b,x=letters)
cat("testing x=letters default:\t\t")
test.equality(b(),letters)

setDefaults(b,x=c('a','b'))
cat("testing x=c('a','b') default:\t\t")
test.equality(b(),c('a','b'))

setDefaults(b,x=a)
cat("testing x=a default:\t\t\t")
test.equality(b(),a)

setDefaults(b,x="a")
cat("testing x='a' default:\t\t\t")
test.equality(b(),"a")

setDefaults(b,x=NULL)
cat("testing x=NULL default:\t\t\t")
test.equality(b(),0)

setDefaults(b,x=list(a=1,b=2))
cat("testing x=list(a=1,b=2) default:\t")
test.equality(b(),list(a=1,b=2))

unDefaults(b)
rm(a,b,test.equality)


