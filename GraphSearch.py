



def iterDepSearch(node1,node2,depth):
    counter = 0
    for d in depth:
        if depthLimitedSearch(node1,node2,d):
            counter =counter +1

def depthLimitedSearch(node1,node2,currentDepthLimit):
    if currentDepthLimit == 0:
        if node1 is node2:
            return [node1,True]
        else:
            return False
    elif currentDepthLimit > 0:
        IsAnyRemainingNode = False

        for node in node2.connectionsObj:
            result = depthLimitedSearch(node1,node,currentDepthLimit-1)

            if result == True:
                return True







