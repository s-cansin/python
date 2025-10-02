def bisectionmethod(eq,bottom_lwl,top_lwl,hata = 0.01):
    fu=eq(top_lwl)
    if fu==0.0 : return top_lwl
    fl=eq(bottom_lwl)
    if fl==0.0 : return bottom_lwl
    else:
        mid=(bottom_lwl+top_lwl)/2
        err1=(top_lwl-bottom_lwl)/2
        fm = mid
        while(err1>hata):
            fu=eq(top_lwl)
            fl=eq(bottom_lwl)
            if fm==0.0 :
                return mid
            elif fu*fm < 0.0 :
                bottom_lwl = mid
            elif fl*fm < 0.0 :
                top_lwl = mid
            mid=(bottom_lwl + top_lwl)/2
            err1=(top_lwl - bottom_lwl)/2
        return mid
def func(mid2):          
    kartb1 = monthlygrossdebt - mid2
    result1 = kartb1 + (interest/100)
    return result1

remainingdebt = float(input("Enter Principal Amount:"))
interest = float(input("Enter Monthly Interest Rate [percentage value with a dot]:"))
maturity = 12 ### WE ENTERED THE NUMBER OF MONTHS IN WHICH THE DEBT WILL BE DISTRIBUTED (MONTHS IN 1 YEAR) AS A VARIABLE..
yedek = 0
for i in range(0,maturity): ### THIS BLOCK IS THE PART OF APPLYING COMPOUND INTEREST TO THE PRINCIPAL..
	taksit=float(remainingdebt/(maturity - i))
	yedek += taksit 	### X. MONTH'S DEBT IS HELD (INTEREST WILL NOT BE ACCRUED FOR THE FIRST MONTH)
	remainingdebt = remainingdebt - taksit	### ALL REMAINING DEBT AFTER MONTH X IS BEING DETERMINED
	remainingdebt = remainingdebt + ((remainingdebt * interest)/100) ### ALL DEBT ENTRY AFTER MONTH X IS SUBJECT TO THE INTEREST PERCENTAGE

remainingdebt = yedek
monthlygrossdebt = remainingdebt/maturity
monthlyincreased = monthlygrossdebt%float(0.01)
if monthlyincreased>0:
	monthlygrossdebt = (float(0.01) - monthlyincreased) + monthlygrossdebt  ### WE ARE TURNING EACH MONTHLY DEBT AMOUNT TO A BIGGER NUMBER DIVIDED BY #0.01 FLOAT NUMBER
a = monthlygrossdebt - 10
b = monthlygrossdebt + 10
result = bisectionmethod(func, a, b)
print "Payment Plan: ", result," USD x ", maturity," MONTH