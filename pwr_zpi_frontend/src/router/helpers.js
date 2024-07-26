
export function prefixRoutes (prefix, routes) {
    return routes.map( (route) => {
        route.path = prefix + '/' + route.path;
        return route;
    })
}
