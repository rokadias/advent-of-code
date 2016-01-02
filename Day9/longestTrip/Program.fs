namespace fullTrip

open System
open System.Linq
open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let lines = Helper.readLines(argv.[0])
        let mutable fullMap = Map.empty<string, Map<string, int>>
        let mutable fullDestinations = Set.empty<string>

        let addSrcDest source destination cost =
            let mutable destMap = Map.empty<string, int>
            if fullMap.ContainsKey(source) then
                destMap <- fullMap.[source]
            if not (destMap.ContainsKey destination && destMap.[destination] < cost) then
                destMap <- destMap.Add(destination, (int cost))
                fullDestinations <- fullDestinations.Add source
                fullDestinations <- fullDestinations.Add destination
                fullMap <- fullMap.Add(source, destMap)

        let fillMap = function
            | Regex @"([A-Za-z]+) to ([A-Za-z]+) = (\d+)" [source; destination; cost] ->
                addSrcDest source destination (int cost)
                addSrcDest destination source (int cost)
            | n -> failwith "Can't recognize line for fillMap"

        Seq.iter fillMap lines

        let mutable highestCost = 0
        let rec calcCost source (path:Set<string>) cost =
            let destMap = fullMap.[source]
            for kvp in destMap do
                if not (path.Contains kvp.Key) then
                    let newPath = path.Add kvp.Key
                    let newCost = cost + kvp.Value
                    if newPath.Count = fullDestinations.Count then
                        if newCost > highestCost then
                            highestCost <- newCost
                    elif fullMap.ContainsKey kvp.Key then
                        calcCost kvp.Key newPath newCost

        let firstKey = fullMap.First().Key
        Set.filter fullMap.ContainsKey fullDestinations
        |> Set.iter (fun key -> calcCost key (Set.empty<string>.Add key) 0)
        printfn "Higheset Cost: %d" highestCost
        0
